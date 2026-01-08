import time
from datetime import datetime
from .mongodb import mongo_connection
import logging

logger = logging.getLogger(__name__)

class APILoggingMiddleware:
    """
    Middleware to log API requests to MongoDB
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Record start time
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Log to MongoDB if it's a train search request
        if request.path.startswith('/api/trains/search/') and request.method == 'GET':
            self.log_to_mongodb(request, execution_time)
        
        return response

    def log_to_mongodb(self, request, execution_time):
        try:
            if not mongo_connection.is_connected():
                logger.warning("MongoDB not connected. Skipping log.")
                return

            user_id = None
            if hasattr(request, 'user') and request.user.is_authenticated:
                user_id = request.user.id

            log_data = {
                'endpoint': request.path,
                'method': request.method,
                'params': dict(request.GET),
                'user_id': user_id,
                'execution_time': execution_time,
                'timestamp': datetime.utcnow(),
                'source': request.GET.get('source'),
                'destination': request.GET.get('destination'),
            }

            db = mongo_connection.db
            db.api_logs.insert_one(log_data)
            
        except Exception as e:
            logger.error(f"Error logging to MongoDB: {e}")