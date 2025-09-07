from app.models.distance_matrix import DistanceMatrix
from app.models.route_response import RouteGroup
from app.services.held_karp_tsp_solver import HeldKarpTspSolver
from app.services.nearest_neighbour_solver import NearestNeighbourRoute
from app.services.or_tools_solver import OrToolsSolver
from app.services.shortestpath_calc import ShortestPathCalculator
from loguru import logger

class ShortestPathCalcFactory:

    NEAREST_NEIGHBOUR = "nearest_neighbour"
    TSP = "tsp"
    OR_TOOLS = "or"

    _providers: dict[str, ShortestPathCalculator] = {
        NEAREST_NEIGHBOUR: NearestNeighbourRoute(),
        TSP: HeldKarpTspSolver(),
        OR_TOOLS: OrToolsSolver()
    }

    @classmethod
    def get_calculator(cls, no_routes:int) -> ShortestPathCalculator:
        if no_routes <= 20:
            name = cls.TSP
        elif no_routes <= 100:
            name = cls.OR_TOOLS
        else:
            name = cls.NEAREST_NEIGHBOUR
        logger.debug(f"ShortestPathCalcFactory will use `{name}` provider")
        return cls._providers.get(name)


    def get_shortest_path(self, distance_matrix: DistanceMatrix, return_to_start: bool) -> RouteGroup:
        logger.debug(f"computing shortest paths for the given distance matrix: {distance_matrix.distances}")
        logger.debug(f"computing shortest paths for the given duration matrix: {distance_matrix.durations}")
        shortest_path_finder = self.get_calculator(len(distance_matrix.distances))
        logger.info(f"computing shortest paths using  {shortest_path_finder.__class__.__name__}...")
        locations = distance_matrix.snapped_locations
        shortest_distance = shortest_path_finder.compute_path(distance_matrix.distances, distance_matrix.durations,
                                                              locations, "distance",
                                                              return_to_start)
        shortest_duration = shortest_path_finder.compute_path(distance_matrix.distances, distance_matrix.durations,
                                                              locations, "duration",
                                                              return_to_start)
        shortest_blended = shortest_path_finder.compute_path(distance_matrix.distances, distance_matrix.durations,
                                                             locations, "blended",
                                                             return_to_start)
        logger.info(f"computed shortest paths using  {shortest_path_finder.__class__.__name__}...")
        return RouteGroup(
            shortest_distance=shortest_distance,
            shortest_duration=shortest_duration,
            shortest_blended=shortest_blended
        )
