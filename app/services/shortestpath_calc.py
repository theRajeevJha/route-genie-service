from abc import ABC, abstractmethod

from app.models.location import Location
from app.models.route_response import RouteDetail


class ShortestPathCalculator(ABC):
    """
    class for shortest path calculation.

    Subclasses must implement the method `compute_path` to compute
    the shortest route based on a given matrix.
    """
    @abstractmethod
    def compute_path(self, distance_matrix:list[list[float]], duration_matrix:list[list[float]], locations:list[Location], route_type:str, return_to_start:bool) -> RouteDetail:
        """
        computes the shortest path for the given distance matrix, duration matrix.
        Args:
            distance_matrix: the distance matrix representing the graph.
            duration_matrix: the duration matrix representing the graph.
            locations: list of locations corresponding to the distance/duration matrices
            route_type: type of route to compute ("distance", "duration", or "blended")
            return_to_start: whether to return to the start location
        Returns:
            RouteDetail: The computed shortest route detail.
        """
        pass