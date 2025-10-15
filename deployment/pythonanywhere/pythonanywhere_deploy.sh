#!/bin/bash
# ============================================================================
# COLLECTORIUM - PYTHONANYWHERE AUTO DEPLOYMENT SCRIPT
# ============================================================================
# Usage: bash pythonanywhere_deploy.sh
# ============================================================================

set -e  # Exit on error

echo "🚀 Collectorium PythonAnywhere Deployment Starting..."
echo "============================================================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="python3.11"
VENV_NAME="collectorium-env"
PROJECT_DIR="$HOME/Collectorium"

# ============================================================================
# STEP 1: Virtual Environment
# ============================================================================
echo -e "${BLUE}[1/7] Creating Virtual Environment...${NC}"

if [ -d "$HOME/.virtualenvs/$VENV_NAME" ]; then
    echo "Virtual environment already exists. Removing old one..."
    rm -rf "$HOME/.virtualenvs/$VENV_NAME"
fi

mkvirtualenv $VENV_NAME --python=$PYTHON_VERSION
workon $VENV_NAME

echo -e "${GREEN}✓ Virtual environment created${NC}"

# ============================================================================
# STEP 2: Install Dependencies
# ============================================================================
echo -e "${BLUE}[2/7] Installing Dependencies...${NC}"

cd $PROJECT_DIR

# Upgrade pip
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
    pip install -e .
else
    echo -e "${YELLOW}Warning: No requirements file found. Installing essential packages...${NC}"
    pip install django django-allauth whitenoise pillow gunicorn mysqlclient
fi

echo -e "${GREEN}✓ Dependencies installed${NC}"

# ============================================================================
# STEP 3: Environment Variables
# ============================================================================
echo -e "${BLUE}[3/7] Setting up Environment Variables...${NC}"

# Create .env file if not exists
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# PythonAnywhere Environment Variables
DJANGO_ENV=production
DEBUG=False
SECRET_KEY=CHANGE_THIS_IN_WEB_TAB
ALLOWED_HOSTS=.pythonanywhere.com

# Database (will be configured via Web tab)
DATABASE_URL=

# Static/Media
STATIC_URL=/static/
MEDIA_URL=/media/

# Email (console for now)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EOF
    echo -e "${YELLOW}⚠ .env file created. You MUST update SECRET_KEY and DATABASE_URL${NC}"
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# ============================================================================
# STEP 4: Collect Static Files
# ============================================================================
echo -e "${BLUE}[4/7] Collecting Static Files...${NC}"

export DJANGO_SETTINGS_MODULE=collectorium.settings.base
python manage.py collectstatic --noinput

echo -e "${GREEN}✓ Static files collected${NC}"

# ============================================================================
# STEP 5: Database Setup
# ============================================================================
echo -e "${BLUE}[5/7] Database Setup...${NC}"

echo -e "${YELLOW}Database configuration must be done via PythonAnywhere Web tab${NC}"
echo -e "${YELLOW}After configuring database, run:${NC}"
echo -e "${YELLOW}  python manage.py migrate${NC}"
echo -e "${YELLOW}  python manage.py createsuperuser${NC}"

# ============================================================================
# STEP 6: WSGI Configuration
# ============================================================================
echo -e "${BLUE}[6/7] WSGI Configuration...${NC}"

cat > $PROJECT_DIR/wsgi_pythonanywhere.py << 'EOF'
"""
WSGI config for Collectorium on PythonAnywhere.

Copy this to your WSGI configuration file in PythonAnywhere Web tab.
"""

import os
import sys

# Add your project directory to the sys.path
path = '/home/YOUR_USERNAME/Collectorium'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'collectorium.settings.base'
os.environ['DJANGO_ENV'] = 'production'

# Activate virtual environment
activate_this = '/home/YOUR_USERNAME/.virtualenvs/collectorium-env/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
EOF

echo -e "${GREEN}✓ WSGI config template created at wsgi_pythonanywhere.py${NC}"
echo -e "${YELLOW}⚠ You must copy this to Web tab WSGI file and replace YOUR_USERNAME${NC}"

# ============================================================================
# STEP 7: Final Instructions
# ============================================================================
echo -e "${BLUE}[7/7] Deployment Complete!${NC}"
echo "============================================================================"
echo -e "${GREEN}✓ Collectorium installed successfully!${NC}"
echo ""
echo -e "${YELLOW}NEXT STEPS (MANUAL):${NC}"
echo ""
echo "1. Go to PythonAnywhere Web tab"
echo "2. Click 'Add a new web app'"
echo "3. Choose 'Manual configuration' → Python 3.11"
echo "4. Set Source code: /home/YOUR_USERNAME/Collectorium"
echo "5. Set Working directory: /home/YOUR_USERNAME/Collectorium"
echo ""
echo "6. WSGI configuration file:"
echo "   - Click on WSGI file link"
echo "   - DELETE all content"
echo "   - COPY content from: $PROJECT_DIR/wsgi_pythonanywhere.py"
echo "   - REPLACE 'YOUR_USERNAME' with your actual username"
echo "   - Save"
echo ""
echo "7. Virtualenv:"
echo "   - Enter: /home/YOUR_USERNAME/.virtualenvs/collectorium-env"
echo ""
echo "8. Static files:"
echo "   URL: /static/  →  Path: /home/YOUR_USERNAME/Collectorium/staticfiles"
echo "   URL: /media/   →  Path: /home/YOUR_USERNAME/Collectorium/media"
echo ""
echo "9. Database (in Databases tab):"
echo "   - Create MySQL database"
echo "   - Update .env with DATABASE_URL"
echo "   - Run: python manage.py migrate"
echo ""
echo "10. Create superuser:"
echo "    - python manage.py createsuperuser"
echo ""
echo "11. Click 'Reload' button in Web tab"
echo ""
echo -e "${GREEN}Your site will be live at: https://YOUR_USERNAME.pythonanywhere.com${NC}"
echo "============================================================================"

