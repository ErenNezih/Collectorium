#!/bin/bash
# ============================================================================
# COLLECTORIUM - PYTHONANYWHERE QUICK COMMANDS
# ============================================================================
# Copy-paste için hazır komutlar
# ============================================================================

# USERNAME'i kendi PythonAnywhere username'inize değiştirin!
USERNAME="erennezih"

echo "=========================================="
echo "COLLECTORIUM PYTHONANYWHERE QUICK SETUP"
echo "=========================================="
echo ""
echo "Aşağıdaki komutları sırayla çalıştırın:"
echo ""

# ============================================================================
# 1. VIRTUAL ENVIRONMENT
# ============================================================================
echo "# 1. Virtual Environment Oluştur"
echo "mkvirtualenv collectorium-env --python=python3.11"
echo ""

# ============================================================================
# 2. DEPENDENCIES
# ============================================================================
echo "# 2. Dependencies Yükle"
echo "pip install --upgrade pip"
echo "pip install -r requirements.txt"
echo "pip install mysqlclient python-dotenv dj-database-url"
echo ""

# ============================================================================
# 3. ENVIRONMENT VARIABLES
# ============================================================================
echo "# 3. SECRET_KEY Oluştur (çıktıyı kopyalayın)"
echo "python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
echo ""

echo "# 4. .env Dosyasını Düzenle"
echo "nano .env.pythonanywhere"
echo "# SECRET_KEY ve Database bilgilerini güncelleyin!"
echo ""

# ============================================================================
# 4. STATIC FILES
# ============================================================================
echo "# 5. Static Files Collect"
echo "export DJANGO_SETTINGS_MODULE=collectorium.settings.pythonanywhere"
echo "python manage.py collectstatic --noinput"
echo ""

# ============================================================================
# 5. DATABASE
# ============================================================================
echo "# 6. Database Migrate"
echo "python manage.py migrate"
echo ""

echo "# 7. Superuser Oluştur"
echo "python manage.py createsuperuser"
echo ""

# ============================================================================
# 6. FIXTURE DATA (Opsiyonel)
# ============================================================================
echo "# 8. Fixture Data Yükle (opsiyonel)"
echo "python manage.py loaddata fixtures/categories.json"
echo ""

# ============================================================================
# VERIFICATION
# ============================================================================
echo "# 9. Kurulumu Test Et"
echo "python manage.py check"
echo ""

echo "=========================================="
echo "WEB TAB AYARLARI:"
echo "=========================================="
echo ""
echo "Source code: /home/$USERNAME/Collectorium"
echo "Working directory: /home/$USERNAME/Collectorium"
echo "Virtualenv: /home/$USERNAME/.virtualenvs/collectorium-env"
echo ""
echo "Static files:"
echo "  URL: /static/  →  Path: /home/$USERNAME/Collectorium/staticfiles"
echo "  URL: /media/   →  Path: /home/$USERNAME/Collectorium/media"
echo ""
echo "WSGI file: pythonanywhere_wsgi.py içeriğini kopyalayın"
echo ""
echo "=========================================="
echo "Site URL: https://$USERNAME.pythonanywhere.com"
echo "=========================================="

