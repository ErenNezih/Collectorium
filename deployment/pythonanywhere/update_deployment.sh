#!/bin/bash
# ============================================================================
# COLLECTORIUM - PYTHONANYWHERE UPDATE SCRIPT
# ============================================================================
# Kullanım: bash update_deployment.sh
# ============================================================================

set -e  # Exit on error

echo "🔄 Collectorium Güncelleniyor..."
echo "============================================================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PROJECT_DIR="$HOME/Collectorium"
VENV_NAME="collectorium-env"

# ============================================================================
# STEP 1: Activate Virtual Environment
# ============================================================================
echo -e "${BLUE}[1/6] Virtual environment aktifleştiriliyor...${NC}"
source ~/.virtualenvs/$VENV_NAME/bin/activate
cd $PROJECT_DIR

# ============================================================================
# STEP 2: Pull Latest Code from GitHub
# ============================================================================
echo -e "${BLUE}[2/6] GitHub'dan son kod çekiliyor...${NC}"
git pull origin main

echo -e "${GREEN}✓ Kod güncellendi${NC}"

# ============================================================================
# STEP 3: Update Dependencies (if requirements changed)
# ============================================================================
echo -e "${BLUE}[3/6] Dependencies kontrol ediliyor...${NC}"
pip install -r requirements-pythonanywhere.txt --upgrade

echo -e "${GREEN}✓ Dependencies güncellendi${NC}"

# ============================================================================
# STEP 4: Database Migrations
# ============================================================================
echo -e "${BLUE}[4/6] Database migrations çalıştırılıyor...${NC}"
python manage.py migrate --noinput

echo -e "${GREEN}✓ Migrations tamamlandı${NC}"

# ============================================================================
# STEP 5: Collect Static Files
# ============================================================================
echo -e "${BLUE}[5/6] Static files toplanıyor...${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}✓ Static files güncellendi${NC}"

# ============================================================================
# STEP 6: Reload Instructions
# ============================================================================
echo -e "${BLUE}[6/6] Web app reload gerekiyor...${NC}"
echo ""
echo -e "${YELLOW}SON ADIM:${NC}"
echo -e "${YELLOW}1. Web tab'a gidin: https://www.pythonanywhere.com/user/$(whoami)/webapps/$(whoami).pythonanywhere.com${NC}"
echo -e "${YELLOW}2. Yeşil 'Reload' butonuna tıklayın${NC}"
echo ""
echo -e "${GREEN}Deployment hazır! Reload'dan sonra siteniz güncel olacak.${NC}"
echo "============================================================================"
echo ""
echo -e "${GREEN}✅ Güncelleme başarılı!${NC}"
echo ""
echo "🌐 Site: https://$(whoami).pythonanywhere.com"
echo "🔧 Admin: https://$(whoami).pythonanywhere.com/admin"
echo ""

