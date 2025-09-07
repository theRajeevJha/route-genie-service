from typing import List
from app.models.distance_matrix import DistanceMatrix
from app.services.route_grouper import RouteGrouper

class SingleRouteGrouper(RouteGrouper):
    """Groups routes into a single route containing all locations."""

    def group_routes(self, distance_matrix: DistanceMatrix) -> List[DistanceMatrix]:
        return [distance_matrix]
