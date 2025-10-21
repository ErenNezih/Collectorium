"""
MySQL Bootstrap for cPanel/Passenger Deployment

This module provides a fallback mechanism for MySQL connectivity.
If mysqlclient fails to install/load (common in shared hosting),
PyMySQL will be used as a drop-in replacement.

Usage:
    Import this module before Django initialization (e.g., in passenger_wsgi.py)
"""

import sys
import warnings

# Attempt to install PyMySQL as MySQLdb replacement
try:
    import pymysql
    
    # Install PyMySQL as MySQLdb
    pymysql.install_as_MySQLdb()
    
    # Optional: Suppress PyMySQL warnings for better compatibility
    from pymysql import converters
    
    # Success message (will appear in Passenger logs if debug enabled)
    # print("[Bootstrap] PyMySQL installed as MySQLdb replacement", file=sys.stderr)
    
except ImportError:
    # PyMySQL not available, will try mysqlclient
    # print("[Bootstrap] PyMySQL not available, using mysqlclient", file=sys.stderr)
    pass

except Exception as e:
    # Unexpected error during bootstrap
    warnings.warn(f"MySQL bootstrap failed: {e}")
    # Don't fail the application, let Django handle database errors
    pass


