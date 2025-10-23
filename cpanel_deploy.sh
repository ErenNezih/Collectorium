#!/bin/bash
# ============================================================================
# 🚀 cPanel Deployment Script
# ============================================================================
# Bu script cPanel'de deployment işlemlerini otomatik olarak yapar
# ============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/home/collecto/collectorium"
VENV_PATH="/home/collecto/virtualenv/collectorium/3.12/bin/activate"
SETTINGS_MODULE="collectorium.settings.hosting"

echo -e "${BLUE}🚀 cPanel Deployment Başlıyor...${NC}"
echo "=========================================="

# Function to print status
print_status() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Step 1: Navigate to project directory
print_status "Proje dizinine geçiliyor..."
cd "$PROJECT_DIR" || {
    print_error "Proje dizini bulunamadı: $PROJECT_DIR"
    exit 1
}
print_success "Proje dizinine geçildi"

# Step 2: Activate virtual environment
print_status "Virtual environment aktifleştiriliyor..."
if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
    print_success "Virtual environment aktifleştirildi"
else
    print_error "Virtual environment bulunamadı: $VENV_PATH"
    exit 1
fi

# Step 3: Set environment variables
print_status "Environment variables ayarlanıyor..."
export DJANGO_SETTINGS_MODULE="$SETTINGS_MODULE"
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"
print_success "Environment variables ayarlandı"

# Step 4: Upgrade pip
print_status "Pip güncelleniyor..."
python -m pip install --upgrade pip
print_success "Pip güncellendi"

# Step 5: Install dependencies
print_status "Dependencies yükleniyor..."
if [ -f "requirements-cpanel.txt" ]; then
    pip install -r requirements-cpanel.txt
    print_success "Dependencies yüklendi (requirements-cpanel.txt)"
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Dependencies yüklendi (requirements.txt)"
else
    print_error "Requirements dosyası bulunamadı"
    exit 1
fi

# Step 6: Check for dependency conflicts
print_status "Dependency conflicts kontrol ediliyor..."
pip check || print_warning "Bazı dependency conflicts var, devam ediliyor..."

# Step 7: Run migrations
print_status "Database migration'ları çalıştırılıyor..."
python manage.py migrate --plan
python manage.py migrate --noinput
print_success "Migration'lar tamamlandı"

# Step 8: Collect static files
print_status "Static files collect ediliyor..."
mkdir -p staticfiles
python manage.py collectstatic --noinput --clear
print_success "Static files collect edildi"

# Step 9: Test database connection
print_status "Database connection test ediliyor..."
if [ -f "scripts/test_db_connection.py" ]; then
    python scripts/test_db_connection.py
    print_success "Database connection test başarılı"
else
    print_warning "Database test script bulunamadı"
fi

# Step 10: Create restart trigger
print_status "Application restart trigger oluşturuluyor..."
mkdir -p tmp
touch tmp/restart.txt
print_success "Restart trigger oluşturuldu"

# Step 11: Final checks
print_status "Final kontroller yapılıyor..."

# Check if manage.py works
python manage.py check --deploy || print_warning "Django check --deploy uyarıları var"

# Check if static files exist
if [ -d "staticfiles" ] && [ "$(ls -A staticfiles)" ]; then
    print_success "Static files mevcut"
else
    print_warning "Static files eksik veya boş"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}🎉 Deployment tamamlandı!${NC}"
echo ""
echo -e "${BLUE}📋 Sonraki adımlar:${NC}"
echo "1. cPanel → Python App → Restart"
echo "2. https://collectorium.com.tr/healthz/ test et"
echo "3. Admin panel: https://collectorium.com.tr/admin/"
echo ""
echo -e "${BLUE}🔍 Test komutları:${NC}"
echo "• Health check: curl https://collectorium.com.tr/healthz/"
echo "• Database test: python scripts/test_db_connection.py"
echo "• Django check: python manage.py check --deploy"
echo ""
echo -e "${GREEN}✅ Deployment başarılı!${NC}"
