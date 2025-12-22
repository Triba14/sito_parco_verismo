#!/bin/bash
# =============================================================================
# first-deploy.sh - Setup Completo VPS Aruba Cloud
# =============================================================================
# Esegui questo script sulla VPS dopo il primo accesso SSH.
# 
# PREREQUISITI:
#   - VPS Aruba Cloud con Ubuntu 22.04 LTS
#   - Accesso SSH come utente con permessi sudo (NON come root!)
#   - Dominio già puntato all'IP della VPS
#
# USAGE:
#   # 1. Scarica lo script
#   curl -O https://raw.githubusercontent.com/Triba14/sito_parco_verismo/main/scripts/first-deploy.sh
#   
#   # 2. Modifica DOMAIN e EMAIL
#   nano first-deploy.sh
#   
#   # 3. Verifica cosa farà (dry-run)
#   chmod +x first-deploy.sh
#   ./first-deploy.sh --check
#   
#   # 4. Esegui per davvero
#   ./first-deploy.sh
# =============================================================================

set -e

# ================================
# CONFIGURAZIONE - MODIFICA QUESTI!
# ================================
DOMAIN="parcovergacapuana.it"
EMAIL="giuseppet100@gmail.com"
REPO_URL="https://github.com/Triba14/sito_parco_verismo.git"
PROJECT_DIR="$HOME/sito_parco_verismo"

# ================================
# COLORI
# ================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ================================
# FUNZIONI
# ================================
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

check_requirements() {
    local errors=0
    
    print_header "🔍 VERIFICA PREREQUISITI"
    
    # 1. Non eseguire come root
    if [[ "$EUID" -eq 0 ]]; then
        print_error "Non eseguire come root! Usa un utente con sudo (es. deploy)"
        echo -e "   Crea utente: ${YELLOW}adduser deploy && usermod -aG sudo deploy${NC}"
        echo -e "   Poi accedi: ${YELLOW}su - deploy${NC}"
        errors=$((errors + 1))
    else
        print_success "Utente non-root: $USER"
    fi
    
    # 2. Verifica sudo
    if ! sudo -n true 2>/dev/null; then
        if ! sudo true; then
            print_error "L'utente $USER non ha permessi sudo"
            errors=$((errors + 1))
        fi
    fi
    print_success "Permessi sudo: OK"
    
    # 3. Verifica sistema operativo
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        if [[ "$ID" == "ubuntu" ]]; then
            print_success "Sistema operativo: $PRETTY_NAME"
        else
            print_warning "Sistema: $PRETTY_NAME (testato su Ubuntu, potrebbe funzionare)"
        fi
    fi
    
    # 4. Verifica connessione internet
    if ping -c 1 github.com &> /dev/null; then
        print_success "Connessione internet: OK"
    else
        print_error "Nessuna connessione internet"
        errors=$((errors + 1))
    fi
    
    # 5. Verifica git
    if command -v git &> /dev/null; then
        print_success "Git installato: $(git --version)"
    else
        print_warning "Git non installato (verrà installato)"
    fi
    
    # 6. Verifica python3
    if command -v python3 &> /dev/null; then
        print_success "Python3 installato: $(python3 --version)"
    else
        print_warning "Python3 non installato (verrà installato)"
    fi
    
    # 7. Verifica spazio disco (minimo 5GB)
    local free_space=$(df -BG / | awk 'NR==2 {print $4}' | tr -d 'G')
    if [[ "$free_space" -ge 5 ]]; then
        print_success "Spazio disco: ${free_space}GB liberi"
    else
        print_error "Spazio disco insufficiente: ${free_space}GB (minimo 5GB)"
        errors=$((errors + 1))
    fi
    
    echo ""
    return $errors
}

# ================================
# VERIFICA CONFIGURAZIONE
# ================================
print_header "🚀 FIRST DEPLOY - Parco Letterario del Verismo"

# Modalità check
if [[ "$1" == "--check" ]]; then
    echo -e "${YELLOW}Modalità verifica (dry-run) - non verrà modificato nulla${NC}\n"
fi

# Verifica DOMAIN
if [[ "$DOMAIN" == "YOUR_DOMAIN.com" ]]; then
    print_error "ERRORE: Modifica DOMAIN nello script!"
    echo -e "Apri lo script con: ${YELLOW}nano first-deploy.sh${NC}"
    echo -e "E modifica la riga: ${YELLOW}DOMAIN=\"tuodominio.com\"${NC}"
    exit 1
fi

# Verifica EMAIL
if [[ "$EMAIL" == "YOUR_EMAIL@example.com" ]]; then
    print_error "ERRORE: Modifica EMAIL nello script!"
    echo -e "Apri lo script con: ${YELLOW}nano first-deploy.sh${NC}"
    echo -e "E modifica la riga: ${YELLOW}EMAIL=\"tua@email.com\"${NC}"
    exit 1
fi

# Verifica formato email
if [[ ! "$EMAIL" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    print_error "ERRORE: EMAIL non valida: $EMAIL"
    exit 1
fi

# Verifica formato dominio
if [[ ! "$DOMAIN" =~ ^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    print_error "ERRORE: DOMAIN non valido: $DOMAIN"
    exit 1
fi

echo -e "Configurazione:"
echo -e "  Dominio: ${GREEN}$DOMAIN${NC}"
echo -e "  Email: ${GREEN}$EMAIL${NC}"
echo -e "  Repository: ${GREEN}$REPO_URL${NC}"
echo -e "  Directory: ${GREEN}$PROJECT_DIR${NC}"
echo ""

# Verifica prerequisiti
if ! check_requirements; then
    print_error "Alcuni prerequisiti non sono soddisfatti. Risolvi gli errori sopra."
    exit 1
fi

# Se modalità check, esci qui
if [[ "$1" == "--check" ]]; then
    print_success "Tutti i controlli passati! Puoi eseguire: ./first-deploy.sh"
    exit 0
fi

read -p "Premi INVIO per continuare o CTRL+C per annullare..."

# ================================
# STEP 1: Aggiornamento Sistema
# ================================
print_header "📦 Step 1/7: Aggiornamento Sistema"

sudo apt update && sudo apt upgrade -y
print_success "Sistema aggiornato"

# Installa dipendenze base
sudo apt install -y git curl python3
print_success "Dipendenze base installate (git, curl, python3)"

# ================================
# STEP 2: Installazione Docker
# ================================
print_header "🐳 Step 2/7: Installazione Docker"

if command -v docker &> /dev/null; then
    print_warning "Docker già installato, salto..."
else
    # Dipendenze Docker
    sudo apt install -y apt-transport-https ca-certificates software-properties-common

    # Repository Docker
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Installazione
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

    # Aggiungi utente al gruppo docker
    sudo usermod -aG docker $USER
    
    print_success "Docker installato"
fi

# Verifica (usa sudo se appena installato)
if command -v docker &> /dev/null; then
    sudo docker --version
    sudo docker compose version
    print_success "Docker funzionante"
fi

# ================================
# STEP 3: Configurazione Firewall
# ================================
print_header "🔥 Step 3/7: Configurazione Firewall"

sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
yes | sudo ufw enable

print_success "Firewall configurato"
sudo ufw status

# ================================
# STEP 4: Clone Repository
# ================================
print_header "📥 Step 4/7: Clone Repository"

if [ -d "$PROJECT_DIR" ]; then
    print_warning "Directory già esistente, aggiorno..."
    cd "$PROJECT_DIR"
    git pull origin main
else
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

print_success "Repository clonato in $PROJECT_DIR"

# ================================
# STEP 5: Configurazione Ambiente
# ================================
print_header "⚙️ Step 5/7: Configurazione Ambiente"

# Genera SECRET_KEY
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')

# Crea .env.production se non esiste
if [ ! -f ".env.production" ] || grep -q "CHANGE-THIS" .env.production; then
    cat > .env.production << EOF
# =============================================================================
# .env.production - Generato automaticamente da first-deploy.sh
# =============================================================================

# --- DJANGO CORE ---
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN

# --- FILES ---
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media

# --- SECURITY ---
SECURE_SSL_REDIRECT=False

# --- GOOGLE ANALYTICS (opzionale) ---
GA_MEASUREMENT_ID=
EOF
    print_success "File .env.production creato"
else
    print_warning ".env.production già configurato, salto..."
fi

# Aggiorna nginx config con dominio
sed -i "s/YOUR_DOMAIN.com/$DOMAIN/g" nginx/conf.d/default.conf
sed -i "s/YOUR_DOMAIN.com/$DOMAIN/g" scripts/ssl-setup.sh
sed -i "s/YOUR_EMAIL@example.com/$EMAIL/g" scripts/ssl-setup.sh

print_success "Configurazione aggiornata con dominio $DOMAIN"

# ================================
# STEP 6: Avvio Container (HTTP)
# ================================
print_header "🚀 Step 6/7: Avvio Container"

# Funzione per eseguire docker compose (con fallback a sudo)
run_docker_compose() {
    if groups | grep -q docker; then
        # L'utente è nel gruppo docker
        if sg docker -c "docker compose $*" 2>/dev/null; then
            return 0
        fi
    fi
    # Fallback: usa sudo
    sudo docker compose $*
}

# Build e avvio
run_docker_compose up -d --build

print_success "Container avviati"

# Attendi che i container siano pronti
echo "Attendo che i container siano pronti..."
sleep 15

# Verifica stato container
echo ""
run_docker_compose ps

# Verifica che il sito risponda
echo ""
echo -e "${YELLOW}Verifico che il sito risponda...${NC}"
if curl -sf http://localhost > /dev/null 2>&1; then
    print_success "Il sito risponde correttamente!"
else
    print_warning "Il sito non risponde ancora. Controlla i log con: docker compose logs -f"
fi

# ================================
# STEP 7: Istruzioni Finali
# ================================
print_header "✅ DEPLOY COMPLETATO!"

echo -e "Il sito è ora accessibile via HTTP: ${GREEN}http://$DOMAIN${NC}"
echo ""
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  PROSSIMI PASSI (in ordine)${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo -e "${BLUE}1. LOGOUT E LOGIN${NC} (per applicare gruppo docker)"
echo -e "   exit"
echo -e "   ssh deploy@IP_VPS"
echo ""
echo -e "${BLUE}2. VERIFICA SITO${NC}"
echo -e "   curl http://localhost"
echo -e "   # Oppure apri http://$DOMAIN nel browser"
echo ""
echo -e "${BLUE}3. ATTIVA SSL/HTTPS${NC}"
echo -e "   cd $PROJECT_DIR"
echo -e "   chmod +x scripts/ssl-setup.sh"
echo -e "   ./scripts/ssl-setup.sh"
echo ""
echo -e "${BLUE}4. CREA SUPERUSER DJANGO${NC}"
echo -e "   docker compose exec web python manage.py createsuperuser"
echo ""
echo -e "${BLUE}5. BACKUP AUTOMATICO${NC}"
echo -e "   chmod +x scripts/backup.sh"
echo -e "   mkdir -p ~/backups"
echo -e "   (crontab -l 2>/dev/null; echo \"0 2 * * * $PROJECT_DIR/scripts/backup.sh\") | crontab -"
echo ""
echo -e "${BLUE}6. GITHUB ACTIONS (opzionale)${NC}"
echo -e "   Vedi docs/DEPLOY.md sezione 13"
echo ""
print_success "Script completato!"
echo ""
echo -e "${GREEN}La SECRET_KEY è stata salvata in .env.production${NC}"
echo -e "${RED}NON condividere questo file!${NC}"

