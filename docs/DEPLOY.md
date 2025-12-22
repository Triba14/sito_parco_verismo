# 🚀 Guida al Deployment su VPS Aruba Cloud

Questa guida ti accompagna nel deployment del **Parco Letterario del Verismo** su una VPS Aruba Cloud.

> [!TIP]
> La maggior parte del processo è **automatizzato** dallo script `first-deploy.sh`. Questa guida spiega i passaggi manuali rimanenti.

---

## 📋 Prerequisiti

| Requisito | Descrizione |
|-----------|-------------|
| **VPS Aruba Cloud** | Piano base (1 vCPU, 2GB RAM, 20GB SSD) |
| **Sistema Operativo** | Ubuntu 22.04 LTS |
| **Dominio** | Un dominio già acquistato (es. parcoverismo.it) |
| **DNS configurato** | Record A che punta all'IP della VPS |

---

## 🚀 Deploy Rapido (5 minuti)

### Step 1: Connettiti alla VPS

```bash
ssh root@93.186.254.13
```

### Step 2: Crea l'utente deploy

```bash
# Crea utente
adduser deploy
# Ti chiederà una password - scegli una sicura!

# Dai permessi sudo
usermod -aG sudo deploy

# Passa all'utente deploy
su - deploy
```

### Step 3: Scarica lo script

> [!NOTE]
> Lo script è già configurato con `DOMAIN="parcovergacapuana.it"` - non devi modificare nulla!

```bash
# Scarica lo script
curl -O https://raw.githubusercontent.com/Triba14/sito_parco_verismo/main/scripts/first-deploy.sh

# Rendi eseguibile
chmod +x first-deploy.sh
```

### Step 4: Esegui lo script

```bash
# (Opzionale) Verifica prima che tutto sia ok
./first-deploy.sh --check

# Esegui il deploy
./first-deploy.sh
```

Lo script automaticamente:
- ✅ Aggiorna il sistema
- ✅ Installa Docker
- ✅ Configura il firewall
- ✅ Clona il repository
- ✅ Genera SECRET_KEY sicura
- ✅ Avvia i container

**Tempo stimato: 3-5 minuti**

---

## 🔐 Step 5: Attiva SSL/HTTPS

> [!IMPORTANT]
> Esegui questo step **solo dopo** che il sito è accessibile via HTTP (http://tuodominio.com)

```bash
cd ~/sito_parco_verismo
chmod +x scripts/ssl-setup.sh
./scripts/ssl-setup.sh
```

Poi modifica manualmente la configurazione Nginx:

```bash
nano nginx/conf.d/default.conf
```

1. **Decommenta** il blocco HTTPS (righe 81-140)
2. **Commenta** la sezione HTTP location / (righe 36-46)
3. **Decommenta** il redirect HTTP → HTTPS (righe 31-33)

```bash
docker compose restart nginx
```

---

## 👤 Step 6: Crea l'admin

```bash
docker compose exec web python manage.py createsuperuser
```

Poi accedi a: `https://tuodominio.com/admin/`

---

## 💾 Step 7: Configura Backup Automatico

```bash
chmod +x scripts/backup.sh
mkdir -p ~/backups

# Aggiungi al cron (backup ogni notte alle 2:00)
(crontab -l 2>/dev/null; echo "0 2 * * * ~/sito_parco_verismo/scripts/backup.sh") | crontab -
```

---

## 🔄 GitHub Actions (Deploy Automatico)

Per aggiornare il sito da GitHub senza accedere alla VPS:

### 1. Genera chiave SSH sulla VPS

```bash
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_actions -N ""
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
cat ~/.ssh/github_actions  # Copia questa chiave privata
```

### 2. Configura GitHub Secrets

Vai su **GitHub → Repository → Settings → Secrets → Actions**

| Secret | Valore |
|--------|--------|
| `VPS_HOST` | IP della VPS (es. `93.186.254.13`) |
| `VPS_USER` | `deploy` |
| `VPS_SSH_KEY` | Chiave privata copiata sopra |
| `VPS_PATH` | `/home/deploy/sito_parco_verismo` |

### 3. Come fare deploy

1. Vai su **GitHub → Actions → Deploy to Production**
2. Clicca **"Run workflow"**
3. Scrivi `deploy` nel campo conferma
4. Clicca **"Run workflow"**

---

## 📊 Comandi Utili

```bash
# Stato container
docker compose ps

# Log in tempo reale
docker compose logs -f

# Riavvia servizi
docker compose restart

# Ricostruisci dopo modifiche
docker compose up -d --build

# Backup manuale
./scripts/backup.sh

# Shell Django
docker compose exec web python manage.py shell
```

---

## ❓ Troubleshooting

### Il sito non si carica
```bash
docker compose ps          # Verifica container attivi
docker compose logs -f     # Controlla errori
sudo ufw status            # Verifica firewall
```

### Errore 502 Bad Gateway
```bash
docker compose logs web    # Controlla errori Django
docker compose restart     # Riavvia tutto
```

### SSL non funziona
```bash
docker compose run --rm certbot certificates  # Verifica certificato
./scripts/ssl-setup.sh                        # Rigenera certificato
```

### Permessi Docker
```bash
# Se "permission denied" con docker
exit
ssh deploy@IP_VPS  # Riconnettiti per applicare gruppo docker
```

---

## 📁 Struttura File

```
sito_parco_verismo/
├── .env.production          # ⚙️ Variabili ambiente (NON su Git!)
├── docker-compose.yml       # 🐳 Orchestrazione container
├── Dockerfile               # 🐳 Build Django
├── nginx/
│   └── conf.d/default.conf  # 🌐 Config Nginx + SSL
├── scripts/
│   ├── first-deploy.sh      # 🚀 Setup automatico VPS
│   ├── ssl-setup.sh         # 🔐 Setup Let's Encrypt
│   └── backup.sh            # 💾 Backup automatico
└── .github/workflows/
    └── deploy.yml           # 🔄 CI/CD GitHub Actions
```

---

*Ultimo aggiornamento: Dicembre 2024*
