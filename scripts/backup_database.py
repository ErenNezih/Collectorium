#!/usr/bin/env python
"""
Database Backup Script

Creates a backup of the Collectorium database.
Supports both PostgreSQL and MySQL databases.

Usage:
    python scripts/backup_database.py [--output-dir /path/to/backups]
"""

import os
import sys
import django
import subprocess
from datetime import datetime
import argparse

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')

try:
    django.setup()
except Exception as e:
    print(f"❌ Failed to initialize Django: {e}")
    sys.exit(1)

from django.conf import settings


def backup_database(output_dir=None):
    """Create database backup"""
    print("=" * 60)
    print("DATABASE BACKUP")
    print("=" * 60)
    print()
    
    # Get database configuration
    db_config = settings.DATABASES['default']
    db_engine = db_config['ENGINE']
    db_name = db_config.get('NAME')
    db_user = db_config.get('USER')
    db_password = db_config.get('PASSWORD')
    db_host = db_config.get('HOST', 'localhost')
    db_port = db_config.get('PORT')
    
    print(f"Database: {db_name}")
    print(f"Engine: {db_engine}")
    print(f"Host: {db_host}")
    print()
    
    # Set output directory
    if not output_dir:
        output_dir = os.path.expanduser('~/backups')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"collectorium_{timestamp}.sql"
    backup_path = os.path.join(output_dir, backup_filename)
    
    print(f"Backup file: {backup_path}")
    print()
    
    # Backup based on database engine
    if 'postgresql' in db_engine:
        print("Backing up PostgreSQL database...")
        return backup_postgresql(db_name, db_user, db_password, db_host, db_port, backup_path, output_dir)
    
    elif 'mysql' in db_engine:
        print("Backing up MySQL database...")
        return backup_mysql(db_name, db_user, db_password, db_host, db_port, backup_path, output_dir)
    
    else:
        print(f"❌ Unsupported database engine: {db_engine}")
        return False


def backup_postgresql(db_name, db_user, db_password, db_host, db_port, backup_path, output_dir):
    """Backup PostgreSQL database using pg_dump"""
    try:
        # Set environment variable for password
        env = os.environ.copy()
        if db_password:
            env['PGPASSWORD'] = db_password
        
        # Build pg_dump command
        cmd = [
            'pg_dump',
            '-h', db_host,
            '-U', db_user,
            '-d', db_name,
            '-F', 'p',  # Plain text SQL
            '-f', backup_path
        ]
        
        if db_port:
            cmd.extend(['-p', str(db_port)])
        
        # Run pg_dump
        print("Running pg_dump...")
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ pg_dump failed: {result.stderr}")
            return False
        
        print(f"✅ Backup created: {backup_path}")
        
        # Compress backup
        print("Compressing backup...")
        compress_result = subprocess.run(
            ['gzip', backup_path],
            capture_output=True,
            text=True
        )
        
        if compress_result.returncode == 0:
            compressed_path = f"{backup_path}.gz"
            print(f"✅ Backup compressed: {compressed_path}")
            
            # Get file size
            size_mb = os.path.getsize(compressed_path) / (1024 * 1024)
            print(f"   Size: {size_mb:.2f} MB")
        else:
            print("⚠️  Compression failed, but backup was created")
        
        # Clean up old backups (keep last 30)
        cleanup_old_backups(output_dir, keep=30)
        
        return True
        
    except FileNotFoundError:
        print("❌ pg_dump not found. Install PostgreSQL client tools.")
        return False
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False


def backup_mysql(db_name, db_user, db_password, db_host, db_port, backup_path, output_dir):
    """Backup MySQL database using mysqldump"""
    try:
        # Build mysqldump command
        cmd = [
            'mysqldump',
            '-h', db_host,
            '-u', db_user,
        ]
        
        if db_password:
            cmd.append(f'--password={db_password}')
        
        if db_port:
            cmd.extend(['-P', str(db_port)])
        
        cmd.extend([
            '--single-transaction',
            '--quick',
            '--lock-tables=false',
            db_name
        ])
        
        # Run mysqldump
        print("Running mysqldump...")
        with open(backup_path, 'w') as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True
            )
        
        if result.returncode != 0:
            print(f"❌ mysqldump failed: {result.stderr}")
            return False
        
        print(f"✅ Backup created: {backup_path}")
        
        # Compress backup
        print("Compressing backup...")
        compress_result = subprocess.run(
            ['gzip', backup_path],
            capture_output=True,
            text=True
        )
        
        if compress_result.returncode == 0:
            compressed_path = f"{backup_path}.gz"
            print(f"✅ Backup compressed: {compressed_path}")
            
            # Get file size
            size_mb = os.path.getsize(compressed_path) / (1024 * 1024)
            print(f"   Size: {size_mb:.2f} MB")
        else:
            print("⚠️  Compression failed, but backup was created")
        
        # Clean up old backups (keep last 30)
        cleanup_old_backups(output_dir, keep=30)
        
        return True
        
    except FileNotFoundError:
        print("❌ mysqldump not found. Install MySQL client tools.")
        return False
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False


def cleanup_old_backups(backup_dir, keep=30):
    """Remove old backup files, keeping the most recent ones"""
    try:
        # Get all backup files
        backup_files = [
            f for f in os.listdir(backup_dir)
            if f.startswith('collectorium_') and (f.endswith('.sql') or f.endswith('.sql.gz'))
        ]
        
        # Sort by creation time (oldest first)
        backup_files.sort(key=lambda f: os.path.getctime(os.path.join(backup_dir, f)))
        
        # Remove old backups
        if len(backup_files) > keep:
            to_remove = backup_files[:-keep]
            print(f"\nCleaning up old backups (keeping last {keep})...")
            
            for filename in to_remove:
                filepath = os.path.join(backup_dir, filename)
                os.remove(filepath)
                print(f"  Removed: {filename}")
            
            print(f"✅ Cleaned up {len(to_remove)} old backup(s)")
    
    except Exception as e:
        print(f"⚠️  Could not clean up old backups: {e}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Backup Collectorium database')
    parser.add_argument(
        '--output-dir',
        help='Directory to store backups (default: ~/backups)',
        default=None
    )
    args = parser.parse_args()
    
    try:
        success = backup_database(output_dir=args.output_dir)
        
        print("\n" + "=" * 60)
        if success:
            print("BACKUP: ✅ COMPLETED")
        else:
            print("BACKUP: ❌ FAILED")
        print("=" * 60)
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Backup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()


