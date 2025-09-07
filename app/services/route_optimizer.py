import time

from app.models.route_request import RouteRequest
from app.models.route_response import RouteResponse
from app.services.route_grouper_factory import RouteGrouperFactory
from app.services.distance_provider_factory import DistanceProviderFactory
from loguru import logger

from app.services.shortest_path_calc_factory import ShortestPathCalcFactory


class RouteOptimizer:
    """ Service to optimize routes using distance provider, route grouper, and shortest path calculator. """

    def __init__(self, distance_provider_name: str = "ors", route_grouper_name: str = "default"):
        self.distance_provider = DistanceProviderFactory.get_providers(distance_provider_name)
        self.route_grouper = RouteGrouperFactory.get_grouper(route_grouper_name)
        self.shortest_path_calc = ShortestPathCalcFactory()

    """
     Optimize routes based on the provided route request details. 
        Steps:
        1. Get distance matrix from distance provider
        2. Group distance matrix into multiple distance matrices if require
        3. Calculate shortest path using shortest path calculator for each distance matrix
        Returns a RouteResponse object with optimized route groups.
    """
    async def optimize_route(self, route_request: RouteRequest) -> RouteResponse:
        logger.info("getting distance matrix...")
        start_time = time.time()
        distance_matrix = await self.distance_provider.get_distance_matrix(route_request)
        elapsed_time = time.time() - start_time
        logger.info(f"distance matrix obtained.total time taken: {elapsed_time:.2f} seconds")

        logger.info("grouping routes...")
        start_time = time.time()
        distance_matrices = self.route_grouper.group_routes(distance_matrix)
        elapsed_time = time.time() - start_time
        logger.info(f"routes grouped into {len(distance_matrices)} parts. total time taken: {elapsed_time:.2f} seconds")

        logger.info("calculating shortest path for each group...")
        start_time = time.time()
        route_groups = []
        for distance_matrix in distance_matrices:
            shortest_routes = self.shortest_path_calc.get_shortest_path(distance_matrix, True)
            route_groups.append(shortest_routes)
        elapsed_time = time.time() - start_time
        logger.info(f"shortest path calculated for all groups. total time taken: {elapsed_time:.2f} seconds")

        return RouteResponse(
            start_location = route_request.start,
            route_groups = route_groups,
            mode = route_request.mode
        )
