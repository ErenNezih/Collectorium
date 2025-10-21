#!/usr/bin/env python
"""
Email Configuration Test Script

Tests email sending functionality for Collectorium.

Usage:
    python scripts/test_email.py [recipient@example.com]
"""

import os
import sys
import django

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')

try:
    django.setup()
except Exception as e:
    print(f"❌ Failed to initialize Django: {e}")
    sys.exit(1)

from django.core.mail import send_mail
from django.conf import settings


def test_email(recipient=None):
    """Test email sending"""
    print("=" * 60)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 60)
    
    # Display email configuration
    print(f"\nEmail Configuration:")
    print(f"  Backend: {settings.EMAIL_BACKEND}")
    print(f"  Host: {settings.EMAIL_HOST}")
    print(f"  Port: {settings.EMAIL_PORT}")
    print(f"  Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"  Use SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
    print(f"  Host User: {settings.EMAIL_HOST_USER}")
    print(f"  From Email: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    # Check if email is configured
    if not settings.EMAIL_HOST_USER and settings.EMAIL_HOST != 'localhost':
        print("⚠️  Email may not be fully configured")
        print("   Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in environment")
        print()
    
    # Determine recipient
    if not recipient:
        if len(sys.argv) > 1:
            recipient = sys.argv[1]
        else:
            recipient = input("Enter recipient email address: ").strip()
    
    if not recipient:
        print("❌ No recipient email provided")
        return False
    
    # Send test email
    print(f"Sending test email to: {recipient}")
    print("Please wait...")
    print()
    
    try:
        send_mail(
            subject='Collectorium Test Email',
            message='This is a test email from Collectorium.\n\n'
                    'If you received this email, your email configuration is working correctly.\n\n'
                    f'Environment: {settings.DEPLOYMENT_INFO.get("environment", "unknown")}\n'
                    f'Hosting: {settings.DEPLOYMENT_INFO.get("hosting", "unknown")}\n'
                    f'Database: {settings.DEPLOYMENT_INFO.get("database", "unknown")}\n\n'
                    'This is an automated test email. Please do not reply.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        print("✅ Email sent successfully!")
        print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"   To: {recipient}")
        print()
        print("📧 Check your inbox (and spam folder)")
        
        return True
        
    except Exception as e:
        print("❌ Email sending failed!")
        print(f"   Error: {e}")
        print()
        
        # Provide troubleshooting tips
        print("Troubleshooting Tips:")
        print("1. Check EMAIL_HOST, EMAIL_PORT settings")
        print("2. Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")
        print("3. For Gmail: Use App Password, not account password")
        print("4. Check firewall/network allows outbound SMTP")
        print("5. For cPanel: localhost SMTP may require different config")
        
        return False


def main():
    """Main function"""
    try:
        success = test_email()
        
        print("\n" + "=" * 60)
        if success:
            print("EMAIL TEST: ✅ PASSED")
        else:
            print("EMAIL TEST: ❌ FAILED")
        print("=" * 60)
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()


