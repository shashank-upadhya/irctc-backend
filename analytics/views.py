from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .mongodb import mongo_connection
import logging

logger = logging.getLogger(__name__)

class TopRoutesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if not mongo_connection.is_connected():
                return Response({
                    'error': 'Analytics service unavailable'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            db = mongo_connection.db
            
            # Aggregate top routes from MongoDB logs
            pipeline = [
                {
                    '$match': {
                        'source': {'$exists': True, '$ne': None},
                        'destination': {'$exists': True, '$ne': None}
                    }
                },
                {
                    '$group': {
                        '_id': {
                            'source': '$source',
                            'destination': '$destination'
                        },
                        'search_count': {'$sum': 1},
                        'avg_execution_time': {'$avg': '$execution_time'},
                        'last_searched': {'$max': '$timestamp'}
                    }
                },
                {
                    '$sort': {'search_count': -1}
                },
                {
                    '$limit': 5
                },
                {
                    '$project': {
                        '_id': 0,
                        'source': '$_id.source',
                        'destination': '$_id.destination',
                        'search_count': 1,
                        'avg_execution_time': {'$round': ['$avg_execution_time', 4]},
                        'last_searched': 1
                    }
                }
            ]

            results = list(db.api_logs.aggregate(pipeline))
            
            return Response({
                'top_routes': results,
                'total_routes_analyzed': len(results)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching top routes: {e}")
            return Response({
                'error': 'Failed to fetch analytics data',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)