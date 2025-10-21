#!/usr/bin/env python
"""
SSL Certificate Verification Script

Checks if SSL certificate is ready before enabling SECURE_SSL_REDIRECT.
This prevents locking out the site if SSL is not yet configured.

Usage:
    python scripts/verify_ssl_ready.py [domain]
"""

import sys
import socket
import ssl
import argparse
from datetime import datetime


def check_ssl_certificate(domain, port=443):
    """Check if SSL certificate exists and is valid"""
    print(f"Checking SSL certificate for {domain}:{port}...")
    
    try:
        # Create SSL context
        context = ssl.create_default_context()
        
        # Connect to the server
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                # Get certificate
                cert = ssock.getpeercert()
                
                # Extract certificate info
                subject = dict(x[0] for x in cert['subject'])
                issued_to = subject.get('commonName', 'N/A')
                issuer = dict(x[0] for x in cert['issuer'])
                issued_by = issuer.get('organizationName', 'N/A')
                
                # Check expiry
                not_after = cert['notAfter']
                expire_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                days_remaining = (expire_date - datetime.now()).days
                
                # Print certificate info
                print(f"\n✅ SSL Certificate Found!")
                print(f"   Issued to: {issued_to}")
                print(f"   Issued by: {issued_by}")
                print(f"   Expires: {not_after}")
                print(f"   Days remaining: {days_remaining}")
                
                if days_remaining < 30:
                    print(f"\n⚠️  WARNING: Certificate expires in {days_remaining} days!")
                    print("   Consider renewing soon.")
                
                if days_remaining < 0:
                    print("\n❌ ERROR: Certificate has expired!")
                    return False
                
                print(f"\n✅ SSL is ready. SECURE_SSL_REDIRECT can be enabled.")
                return True
                
    except ssl.SSLError as e:
        print(f"\n❌ SSL Error: {e}")
        print("\n⚠️  SSL certificate not ready or invalid.")
        print("   Action: Keep SECURE_SSL_REDIRECT=False until SSL is configured.")
        return False
        
    except socket.gaierror as e:
        print(f"\n❌ DNS Error: {e}")
        print(f"   Cannot resolve {domain}")
        print("   Action: Verify domain is pointing to cPanel server.")
        return False
        
    except ConnectionRefusedError:
        print(f"\n❌ Connection refused to {domain}:{port}")
        print("   Action: Verify server is running and port is open.")
        return False
        
    except socket.timeout:
        print(f"\n❌ Connection timeout to {domain}:{port}")
        print("   Action: Verify server is accessible.")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Verify SSL certificate readiness')
    parser.add_argument(
        'domain',
        nargs='?',
        help='Domain to check (e.g., yourdomain.com)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=443,
        help='Port to check (default: 443)'
    )
    
    args = parser.parse_args()
    
    domain = args.domain
    
    if not domain:
        domain = input("Enter domain to check: ").strip()
    
    if not domain:
        print("❌ No domain provided")
        sys.exit(1)
    
    # Remove protocol if provided
    domain = domain.replace('https://', '').replace('http://', '')
    domain = domain.split('/')[0]  # Remove path if any
    
    print("=" * 60)
    print("SSL CERTIFICATE VERIFICATION")
    print("=" * 60)
    print()
    
    is_ready = check_ssl_certificate(domain, args.port)
    
    print("\n" + "=" * 60)
    
    if is_ready:
        print("RECOMMENDATION: ✅ Enable SECURE_SSL_REDIRECT=True")
        print("\nIn cPanel → Python App → Environment Variables:")
        print("  SECURE_SSL_REDIRECT=True")
    else:
        print("RECOMMENDATION: ⚠️  Keep SECURE_SSL_REDIRECT=False")
        print("\nIn cPanel → Python App → Environment Variables:")
        print("  SECURE_SSL_REDIRECT=False")
        print("\nOnce SSL is configured:")
        print("  1. Run this script again to verify")
        print("  2. Change SECURE_SSL_REDIRECT=True")
        print("  3. Restart application (touch tmp/restart.txt)")
    
    print("=" * 60)
    
    sys.exit(0 if is_ready else 1)


if __name__ == '__main__':
    main()


