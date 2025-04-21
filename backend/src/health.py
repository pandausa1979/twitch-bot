from aiohttp import web
import logging

logger = logging.getLogger(__name__)

async def health_check(request):
    """Basic health check endpoint"""
    return web.json_response({"status": "healthy"})

async def readiness_check(request):
    """Readiness check endpoint that verifies MongoDB connection"""
    try:
        # Get MongoDB client from the app
        mongo_client = request.app['mongo_client']
        # Try to ping the database
        mongo_client.admin.command('ping')
        return web.json_response({"status": "ready"})
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return web.json_response({"status": "not ready"}, status=503)

def setup_health_routes(app, mongo_client):
    """Setup health check routes"""
    app['mongo_client'] = mongo_client
    app.router.add_get('/health', health_check)
    app.router.add_get('/ready', readiness_check) 