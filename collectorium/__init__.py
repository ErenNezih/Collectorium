"""
Collectorium Django Project

This module configures PyMySQL as MySQLdb replacement for MySQL database connectivity.
This allows Django to work with MySQL without requiring system-level MySQL client libraries.
"""

# Configure PyMySQL as MySQLdb replacement
# This must be done before Django imports any MySQL-related modules
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    # PyMySQL not available, will use mysqlclient if available
    pass
