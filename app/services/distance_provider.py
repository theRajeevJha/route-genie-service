from abc import ABC, abstractmethod

from app.models.distance_matrix import DistanceMatrix
from app.models.route_request import RouteRequest

class DistanceProvider(ABC):

    @abstractmethod
    async def get_distance_matrix(self, routes: RouteRequest) -> DistanceMatrix:
        """
        Calculates the distance matrix between routes.
        Args:
            routes: The routes to calculate the distance matrix from.
        returns: The distance matrix as a dictionary.
        """
        pass