#!/bin/bash
# =============================================================================
# backup.sh - Backup Leggero SQLite + Media
# =============================================================================
# Crea backup compressi di:
# - Database SQLite (~pochi KB compressi)
# - File media (opzionale, solo se non troppo grandi)
#
# CRON: Aggiungi al crontab per backup automatici
# 0 2 * * * /path/to/backup.sh >> /var/log/backup.log 2>&1
# =============================================================================

set -e

# ================================
# CONFIGURAZIONE
# ================================
BACKUP_DIR="/home/deploy/backups"
PROJECT_DIR="/home/deploy/sito_parco_verismo"
KEEP_DAYS=7  # Giorni di backup da mantenere
DATE=$(date +%Y%m%d_%H%M%S)

# ================================
# COLORI
# ================================
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[$(date)] Inizio backup...${NC}"

# Crea directory backup se non esiste
mkdir -p "$BACKUP_DIR"

# ================================
# BACKUP DATABASE SQLite
# ================================
echo -e "${YELLOW}Backup database SQLite...${NC}"

# Copia il database dal volume Docker
docker cp parco_verismo_web:/app/data/db.sqlite3 /tmp/db_backup.sqlite3 2>/dev/null || \
docker cp parco_verismo_web:/app/db.sqlite3 /tmp/db_backup.sqlite3

# Comprimi (SQLite da ~400KB diventa ~50KB)
gzip -9 /tmp/db_backup.sqlite3
mv /tmp/db_backup.sqlite3.gz "$BACKUP_DIR/db_${DATE}.sqlite3.gz"

DB_SIZE=$(du -h "$BACKUP_DIR/db_${DATE}.sqlite3.gz" | cut -f1)
echo -e "${GREEN}✓ Database: $DB_SIZE${NC}"

# ================================
# BACKUP MEDIA (opzionale, solo file piccoli)
# ================================
echo -e "${YELLOW}Backup media files...${NC}"

# Calcola dimensione media
MEDIA_SIZE=$(docker exec parco_verismo_web du -sh /app/media 2>/dev/null | cut -f1 || echo "0")

# Se media > 100MB, salta (troppo grande per backup "leggero")
if [[ "$MEDIA_SIZE" == *"G"* ]] || [[ "${MEDIA_SIZE%M}" -gt 100 ]]; then
    echo -e "${YELLOW}⚠ Media troppo grande ($MEDIA_SIZE), backup saltato${NC}"
else
    docker cp parco_verismo_web:/app/media /tmp/media_backup
    tar -czf "$BACKUP_DIR/media_${DATE}.tar.gz" -C /tmp media_backup
    rm -rf /tmp/media_backup
    MEDIA_BACKUP_SIZE=$(du -h "$BACKUP_DIR/media_${DATE}.tar.gz" | cut -f1)
    echo -e "${GREEN}✓ Media: $MEDIA_BACKUP_SIZE${NC}"
fi

# ================================
# PULIZIA VECCHI BACKUP
# ================================
echo -e "${YELLOW}Pulizia backup più vecchi di $KEEP_DAYS giorni...${NC}"
find "$BACKUP_DIR" -name "db_*.sqlite3.gz" -mtime +$KEEP_DAYS -delete
find "$BACKUP_DIR" -name "media_*.tar.gz" -mtime +$KEEP_DAYS -delete

# ================================
# RIEPILOGO
# ================================
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   BACKUP COMPLETATO${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "Directory: $BACKUP_DIR"
echo -e "File creati:"
ls -lh "$BACKUP_DIR"/*_${DATE}* 2>/dev/null || echo "Nessun file"
echo ""
echo -e "Spazio totale backup:"
du -sh "$BACKUP_DIR"
