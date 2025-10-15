#!/bin/bash
# ============================================================================
# COLLECTORIUM - AUTO RELOAD SCRIPT
# ============================================================================
# PythonAnywhere API ile otomatik reload
# ============================================================================

USERNAME=$(whoami)
DOMAIN="$USERNAME.pythonanywhere.com"

# API Token alın: Account → API token
# Sonra bu dosyayı düzenleyip token'ı ekleyin:
API_TOKEN="YOUR_API_TOKEN_HERE"

echo "🔄 Web app reload ediliyor..."

curl -X POST \
  "https://www.pythonanywhere.com/api/v0/user/$USERNAME/webapps/$DOMAIN/reload/" \
  -H "Authorization: Token $API_TOKEN"

echo ""
echo "✅ Reload tamamlandı!"
echo "🌐 https://$DOMAIN"

