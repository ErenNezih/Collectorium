"""
Health check endpoints for Collectorium.
Used for monitoring and deployment verification.
"""

from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import django
import os


def healthz(request):
    """
    Basic health check endpoint.
    Returns 200 if application is running.
    """
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Get Django version
    django_version = django.get_version()
    
    # Check if database is accessible
    is_healthy = db_status == "ok"
    status_code = 200 if is_healthy else 503
    
    # Commit hash: Render sets RENDER_GIT_COMMIT or GIT_COMMIT
    commit_hash = os.environ.get("RENDER_GIT_COMMIT") or os.environ.get("GIT_COMMIT") or "unknown"

    return JsonResponse({
        "status": "healthy" if is_healthy else "unhealthy",
        "database": db_status,
        "django": django_version,
        "commit": commit_hash[:7],
        "debug": settings.DEBUG,
    }, status=status_code)


def readiness(request):
    """
    Readiness probe - checks if app is ready to serve traffic.
    """
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            "status": "ready",
            "checks": {
                "database": "ok",
            }
        })
    except Exception as e:
        return JsonResponse({
            "status": "not_ready",
            "error": str(e)
        }, status=503)


def liveness(request):
    """
    Liveness probe - checks if app is alive.
    """
    return JsonResponse({
        "status": "alive"
    })
