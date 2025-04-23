"""Health check package for monitoring application status."""

from .routes import setup_routes as setup_health_routes

__all__ = ['setup_health_routes'] 