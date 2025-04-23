"""Health check routes for the Twitch bot application."""
import logging
from aiohttp import web
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)

async def health_check(request: web.Request) -> web.Response:
    """
    Basic health check endpoint.
    
    Returns:
        JSON response indicating service health
    """
    return web.json_response({"status": "healthy"})

async def readiness_check(request: web.Request) -> web.Response:
    """
    Readiness check endpoint that verifies MongoDB connection.
    
    Returns:
        JSON response indicating service readiness
    """
    try:
        # Get MongoDB client from the app
        mongo_client: MongoClient = request.app['mongo_client']
        # Try to ping the database
        mongo_client.admin.command('ping')
        return web.json_response({"status": "ready"})
    except ConnectionFailure as e:
        logger.error(f"MongoDB connection failed during readiness check: {str(e)}")
        return web.json_response({"status": "not ready", "reason": "database connection failed"}, status=503)
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return web.json_response({"status": "not ready", "reason": str(e)}, status=503)

def setup_routes(app: web.Application, mongo_client: MongoClient) -> None:
    """
    Setup health check routes.
    
    Args:
        app: The aiohttp application instance
        mongo_client: MongoDB client instance for database checks
    """
    app['mongo_client'] = mongo_client
    app.router.add_get('/health', health_check)
    app.router.add_get('/ready', readiness_check) 