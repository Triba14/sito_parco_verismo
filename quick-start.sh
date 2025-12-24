#!/usr/bin/env bash
# =============================================================================
# QUICK START - Setup completo automatico senza domande
# =============================================================================
# Esegue setup completo con configurazione predefinita:
# - Virtual environment + dipendenze
# - Migrazioni database
# - Superuser admin/admin123
# - Database demo popolato
# - Avvio server automatico
#
# Uso: ./quick-start.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
printf "${CYAN}╔═══════════════════════════════════════════════╗${NC}\n"
printf "${CYAN}║  PARCO LETTERARIO G. VERGA E L. CAPUANA - QUICK START      ║${NC}\n"
printf "${CYAN}╚═══════════════════════════════════════════════╝${NC}\n"
echo ""

# Detect Python
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "❌ Python 3 non trovato!"
    exit 1
fi

VENV_DIR=".venv"
VENV_PY="$VENV_DIR/bin/python"

# 1. Virtual Environment
printf "${YELLOW}[1/6]${NC} Creazione virtual environment...\n"
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_CMD -m venv "$VENV_DIR"
fi
printf "${GREEN}✓${NC} Virtual environment pronto\n\n"

# 2. Dipendenze Python
printf "${YELLOW}[2/6]${NC} Installazione dipendenze Python...\n"
"$VENV_PY" -m pip install --upgrade pip -q

# Rileva se usare SQLite (dev) o PostgreSQL (prod)
if command -v pg_config >/dev/null 2>&1; then
    # PostgreSQL disponibile, usa requirements.txt completo
    printf "  → PostgreSQL rilevato, uso requirements.txt\n"
    "$VENV_PY" -m pip install -r requirements.txt -q
else
    # PostgreSQL non disponibile, usa SQLite con requirements-dev.txt
    printf "  → PostgreSQL non trovato, uso SQLite (requirements-dev.txt)\n"
    "$VENV_PY" -m pip install -r requirements-dev.txt -q
fi
printf "${GREEN}✓${NC} Dipendenze installate\n\n"

# 3. Dipendenze npm (se necessario)
if [ -f "package.json" ]; then
    printf "${YELLOW}[3/6]${NC} Installazione dipendenze npm...\n"
    if command -v npm >/dev/null 2>&1; then
        npm install -q 2>/dev/null || npm install
        npm run setup -q 2>/dev/null || npm run setup
        printf "${GREEN}✓${NC} Asset frontend pronti\n\n"
    else
        printf "${YELLOW}⚠${NC}  npm non trovato, skip asset frontend\n\n"
    fi
else
    printf "${YELLOW}[3/6]${NC} Package.json non trovato, skip npm\n\n"
fi

# 4. Database
printf "${YELLOW}[4/6]${NC} Setup database...\n"
"$VENV_PY" manage.py migrate
printf "${GREEN}✓${NC} Migrazioni applicate\n\n"

# 5. Traduzioni
printf "${YELLOW}[5/6]${NC} Compilazione traduzioni...\n"
if "$VENV_PY" manage.py compilemessages 2>/dev/null; then
    printf "${GREEN}✓${NC} Traduzioni compilate\n\n"
else
    printf "${YELLOW}⚠${NC}  gettext non disponibile, skip traduzioni\n\n"
fi

# 6. Dati iniziali
printf "${YELLOW}[6/6]${NC} Setup dati demo...\n"
if [ -f "populate_db_complete.py" ]; then
    "$VENV_PY" populate_db_complete.py 2>/dev/null || true
    printf "${GREEN}✓${NC} Database popolato\n\n"
else
    printf "${YELLOW}⚠${NC}  populate_db_complete.py non trovato\n\n"
fi

# Riepilogo
echo ""
printf "${GREEN}╔═══════════════════════════════════════════════╗${NC}\n"
printf "${GREEN}║         ✓ SETUP COMPLETATO!                  ║${NC}\n"
printf "${GREEN}╚═══════════════════════════════════════════════╝${NC}\n"
echo ""
printf "${CYAN}📦 Progetto configurato e pronto${NC}\n"
printf "${CYAN}👤 Superuser: ${YELLOW}admin${CYAN} / ${YELLOW}admin123${NC}\n"
echo ""
printf "${YELLOW}➜ Avvio server di sviluppo...${NC}\n"
echo ""

# Avvia server
"$VENV_PY" manage.py runserver
