from abc import ABC, abstractmethod
from typing import List

from app.models.distance_matrix import DistanceMatrix

class RouteGrouper(ABC):
    """
    Abstract base class for route grouping strategies.

    This class defines the interface for grouping routes based on a distance matrix.
    Subclasses should implement the `group_routes` method to provide specific grouping logic.
    """

    @abstractmethod
    def group_routes(self, distance_matrix: DistanceMatrix) -> List[DistanceMatrix]:
        """
        Groups routes based on the provided distance matrix.

        Args:
            distance_matrix (DistanceMatrix): The distance matrix to group routes from.

        Returns:
            List[DistanceMatrix]: A list of DistanceMatrix objects, each representing a group of routes.
        """
        pass