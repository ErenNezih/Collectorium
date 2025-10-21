#!/usr/bin/env python3
"""
🚀 cPanel Otomatik Deployment Script
Local değişiklikleri cPanel'e push eder
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Komut çalıştır ve sonucu göster"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} başarılı")
        if result.stdout:
            print(f"📤 Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} başarısız")
        print(f"📤 Error: {e.stderr.strip()}")
        return False

def check_git_status():
    """Git durumunu kontrol et"""
    print("🔍 Git durumu kontrol ediliyor...")
    
    # Uncommitted changes kontrolü
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("📝 Uncommitted değişiklikler bulundu:")
        print(result.stdout.strip())
        return True
    else:
        print("✅ Tüm değişiklikler commit edilmiş")
        return False

def deploy():
    """Ana deployment fonksiyonu"""
    print("🚀 cPanel Deployment Başlıyor...")
    print("=" * 50)
    
    # 1. Git status kontrolü
    has_changes = check_git_status()
    
    if has_changes:
        print("\n📝 Yeni değişiklikler commit ediliyor...")
        
        # Add all changes
        if not run_command("git add .", "Değişiklikleri staging'e ekleme"):
            return False
            
        # Commit
        commit_msg = input("💬 Commit mesajı girin (Enter = 'Auto deploy'): ").strip()
        if not commit_msg:
            commit_msg = "Auto deploy"
            
        if not run_command(f'git commit -m "{commit_msg}"', "Commit işlemi"):
            return False
    
    # 2. Push to GitHub
    print("\n📤 GitHub'a push ediliyor...")
    if not run_command("git push origin main", "GitHub push"):
        return False
    
    # 3. cPanel deployment bilgisi
    print("\n" + "=" * 50)
    print("🎉 Deployment tamamlandı!")
    print("\n📋 Sonraki adımlar:")
    print("1. cPanel → Git Version Control → collectorium")
    print("2. 'Deploy' butonuna tıklayın")
    print("3. Veya otomatik deploy bekleyin (2-3 dakika)")
    print("\n🌐 Site kontrolü:")
    print("https://collectorium.com.tr/healthz")
    
    return True

if __name__ == "__main__":
    try:
        success = deploy()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Deployment iptal edildi")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Beklenmeyen hata: {e}")
        sys.exit(1)
