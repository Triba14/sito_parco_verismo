"""
Form per validazione Prenotazioni e altri form del sito.
"""
# Standard library imports
import re
from datetime import date, timedelta

# Django imports
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator

# Local imports
from .models import Prenotazione


class PrenotazioneForm(forms.ModelForm):
    """Form validato per le prenotazioni itinerari"""
    
    # Validatori personalizzati
    phone_validator = RegexValidator(
        regex=r'^[\d\s\+\-\(\)]{9,20}$',
        message='Inserisci un numero di telefono valido (9-20 caratteri, solo numeri e simboli +,-, (), spazi)'
    )
    
    class Meta:
        model = Prenotazione
        fields = [
            'nome', 'cognome', 'email', 'telefono', 
            'luogo', 'itinerario', 'data_preferita', 
            'numero_partecipanti', 'messaggio'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mario',
                'required': True,
                'minlength': '2',
                'maxlength': '100',
            }),
            'cognome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rossi',
                'required': True,
                'minlength': '2',
                'maxlength': '100',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'mario.rossi@example.com',
                'required': True,
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+39 123 456 7890',
                'minlength': '9',
                'maxlength': '20',
            }),
            'luogo': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'itinerario': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'data_preferita': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'numero_partecipanti': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '100',
                'value': '1',
                'required': True,
            }),
            'messaggio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Eventuali richieste o informazioni aggiuntive...',
                'maxlength': '1000',
            }),
        }
    
    def clean_nome(self):
        """Validazione campo nome"""
        nome = self.cleaned_data.get('nome', '').strip()
        if not nome:
            raise ValidationError('Il nome è obbligatorio')
        if len(nome) < 2:
            raise ValidationError('Il nome deve contenere almeno 2 caratteri')
        if len(nome) > 100:
            raise ValidationError('Il nome non può superare 100 caratteri')
        # Rimuovi caratteri non validi
        if not re.match(r'^[a-zA-ZàèéìòùÀÈÉÌÒÙ\s\'-]+$', nome):
            raise ValidationError('Il nome contiene caratteri non validi')
        return nome.title()
    
    def clean_cognome(self):
        """Validazione campo cognome"""
        cognome = self.cleaned_data.get('cognome', '').strip()
        if not cognome:
            raise ValidationError('Il cognome è obbligatorio')
        if len(cognome) < 2:
            raise ValidationError('Il cognome deve contenere almeno 2 caratteri')
        if len(cognome) > 100:
            raise ValidationError('Il cognome non può superare 100 caratteri')
        # Rimuovi caratteri non validi
        if not re.match(r'^[a-zA-ZàèéìòùÀÈÉÌÒÙ\s\'-]+$', cognome):
            raise ValidationError('Il cognome contiene caratteri non validi')
        return cognome.title()
    
    def clean_email(self):
        """Validazione e normalizzazione email"""
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError('L\'email è obbligatoria')
        
        # Validazione formato email
        validator = EmailValidator(message='Inserisci un indirizzo email valido')
        try:
            validator(email)
        except ValidationError:
            raise ValidationError('Inserisci un indirizzo email valido (es: nome@dominio.it)')
        
        # Blocca email temporanee/sospette (opzionale)
        domini_bloccati = ['tempmail.com', 'throwaway.email', '10minutemail.com']
        dominio = email.split('@')[1] if '@' in email else ''
        if dominio in domini_bloccati:
            raise ValidationError('Non sono accettate email temporanee')
        
        return email
    
    def clean_telefono(self):
        """Validazione e normalizzazione telefono"""
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono:
            # Il telefono è opzionale ma consigliato
            return ''
        
        # Rimuovi spazi e caratteri speciali per validazione
        telefono_pulito = re.sub(r'[^\d+]', '', telefono)
        
        # Validazione lunghezza
        if len(telefono_pulito) < 9:
            raise ValidationError('Il numero di telefono è troppo corto (minimo 9 cifre)')
        if len(telefono_pulito) > 20:
            raise ValidationError('Il numero di telefono è troppo lungo (massimo 20 cifre)')
        
        # Validazione formato base
        if not re.match(r'^\+?[\d]+$', telefono_pulito):
            raise ValidationError('Il numero di telefono contiene caratteri non validi')
        
        return telefono
    
    def clean_numero_partecipanti(self):
        """Validazione numero partecipanti"""
        numero = self.cleaned_data.get('numero_partecipanti')
        if not numero:
            raise ValidationError('Il numero di partecipanti è obbligatorio')
        if numero < 1:
            raise ValidationError('Deve esserci almeno 1 partecipante')
        if numero > 100:
            raise ValidationError('Il numero massimo di partecipanti è 100. Per gruppi più grandi contattaci direttamente.')
        return numero
    
    def clean_data_preferita(self):
        """Validazione data preferita"""
        data = self.cleaned_data.get('data_preferita')
        if data:
            oggi = date.today()
            if data < oggi:
                raise ValidationError('La data preferita non può essere nel passato')
            # Limite massimo 1 anno in futuro
            max_data = oggi + timedelta(days=365)
            if data > max_data:
                raise ValidationError('La data preferita non può essere oltre 1 anno da oggi')
        return data
    
    def clean_messaggio(self):
        """Validazione messaggio"""
        messaggio = self.cleaned_data.get('messaggio', '').strip()
        if len(messaggio) > 1000:
            raise ValidationError('Il messaggio non può superare 1000 caratteri')
        return messaggio
    
    def clean(self):
        """Validazione complessiva del form"""
        cleaned_data = super().clean()
        
        # Validazione anti-spam: controlla se il messaggio sembra spam
        messaggio = cleaned_data.get('messaggio', '')
        if messaggio:
            # Blocca messaggi con troppi link
            num_link = len(re.findall(r'https?://', messaggio))
            if num_link > 3:
                raise ValidationError('Il messaggio contiene troppi link. Inserisci massimo 3 link.')
            
            # Blocca messaggi solo maiuscole (spam comune)
            if len(messaggio) > 20 and messaggio.isupper():
                raise ValidationError('Non scrivere il messaggio tutto in maiuscolo')
        
        return cleaned_data
