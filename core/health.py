"""
Health Check Endpoints for Collectorium

Provides system health status for monitoring and load balancers.
"""

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import time


def healthz(request):
    """
    Basic health check endpoint.
    
    Returns 200 OK if the application is running.
    Used by load balancers and monitoring systems.
    
    Response:
        {"status": "healthy"}
    """
    return JsonResponse({"status": "healthy"}, status=200)


def readiness(request):
    """
    Readiness probe - checks if app is ready to serve requests.
    
    Checks:
    - Database connectivity
    - Cache availability (if configured)
    
    Returns:
        200 OK if ready
        503 Service Unavailable if not ready
    
    Response:
        {
            "status": "ready|not_ready",
            "checks": {
                "database": "ok|error",
                "cache": "ok|error"
            },
            "timestamp": <unix_timestamp>
        }
    """
    checks = {}
    overall_status = "ready"
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        overall_status = "not_ready"
    
    # Check cache
    try:
        cache_key = "health_check"
        cache_value = "ok"
        cache.set(cache_key, cache_value, 10)
        if cache.get(cache_key) == cache_value:
            checks["cache"] = "ok"
        else:
            checks["cache"] = "error: cache read/write failed"
            overall_status = "not_ready"
    except Exception as e:
        checks["cache"] = f"error: {str(e)}"
        # Cache failure is not critical
    
    status_code = 200 if overall_status == "ready" else 503
    
    return JsonResponse({
        "status": overall_status,
        "checks": checks,
        "timestamp": int(time.time())
    }, status=status_code)


def liveness(request):
    """
    Liveness probe - checks if app is alive (but maybe not ready).
    
    This is a simple check that returns 200 if the process is running.
    Used by orchestrators (Kubernetes, etc.) to decide if to restart the pod.
    
    Response:
        {"status": "alive"}
    """
    return JsonResponse({"status": "alive"}, status=200)

