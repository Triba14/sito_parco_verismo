#!/bin/bash
# =============================================================================
# ssl-setup.sh - Setup SSL con Let's Encrypt
# =============================================================================
# ISTRUZIONI:
# 1. Modifica YOUR_DOMAIN e YOUR_EMAIL qui sotto
# 2. Assicurati che il DNS punti già alla VPS
# 3. Esegui: chmod +x ssl-setup.sh && ./ssl-setup.sh
# =============================================================================

set -e

# ================================
# CONFIGURAZIONE
# ================================
DOMAIN="parcovergacapuana.it"
EMAIL="giuseppet100@gmail.com"

# ================================
# COLORI
# ================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   SSL Setup - Let's Encrypt${NC}"
echo -e "${GREEN}========================================${NC}"

# Verifica configurazione
if [[ "$DOMAIN" == "YOUR_DOMAIN.com" ]]; then
    echo -e "${RED}ERRORE: Modifica DOMAIN e EMAIL nello script!${NC}"
    exit 1
fi

echo -e "${YELLOW}Dominio: ${DOMAIN}${NC}"
echo -e "${YELLOW}Email: ${EMAIL}${NC}"
echo ""

# Step 1: Verifica che Nginx sia in esecuzione
echo -e "${YELLOW}[1/4] Verifico che i container siano attivi...${NC}"
if ! docker compose ps | grep -q "nginx.*Up"; then
    echo -e "${RED}Nginx non è in esecuzione. Avvialo prima con:${NC}"
    echo "docker compose up -d nginx web"
    exit 1
fi
echo -e "${GREEN}✓ Container attivi${NC}"

# Step 2: Ottieni certificato SSL
echo -e "${YELLOW}[2/4] Richiedo certificato SSL a Let's Encrypt...${NC}"
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN" \
    -d "www.$DOMAIN"

echo -e "${GREEN}✓ Certificato ottenuto!${NC}"

# Step 3: Aggiorna configurazione Nginx
echo -e "${YELLOW}[3/4] Aggiorno configurazione Nginx...${NC}"

# Sostituisci YOUR_DOMAIN.com nella config
sed -i "s/YOUR_DOMAIN.com/$DOMAIN/g" nginx/conf.d/default.conf

# Decommentare redirect HTTP -> HTTPS
sed -i 's/# location \/ {/location \/ {/' nginx/conf.d/default.conf
sed -i 's/#     return 301/    return 301/' nginx/conf.d/default.conf
sed -i 's/# }/}/' nginx/conf.d/default.conf

# Decommentare blocco HTTPS (rimuovi # all'inizio delle righe nel blocco HTTPS)
# Questo è fatto manualmente per sicurezza

echo -e "${YELLOW}ATTENZIONE: Devi decommentare manualmente il blocco HTTPS in:${NC}"
echo -e "${YELLOW}nginx/conf.d/default.conf${NC}"
echo ""

# Step 4: Riavvia Nginx
echo -e "${YELLOW}[4/4] Riavvio Nginx...${NC}"
docker compose restart nginx

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   SSL CONFIGURATO CON SUCCESSO!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Prossimi passi:"
echo -e "1. ${YELLOW}Decommenta il blocco HTTPS${NC} in nginx/conf.d/default.conf"
echo -e "2. ${YELLOW}Commenta la sezione HTTP location /${NC} (quella con proxy_pass)"
echo -e "3. Riavvia: ${GREEN}docker compose restart nginx${NC}"
echo -e "4. Verifica: ${GREEN}curl -I https://$DOMAIN${NC}"
echo ""
echo -e "Il certificato si rinnoverà automaticamente ogni 12 ore (gestito da Certbot)."
