from app.models.location import Location
from app.models.route_response import RouteDetail
from app.services.shortestpath_calc import ShortestPathCalculator
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

class OrToolsSolver(ShortestPathCalculator):

    def compute_path(self, distances:list[list[float]], durations:list[list[float]], locations:list[Location], param:str, return_to_start:bool) -> RouteDetail:
        n = len(distances)
        if n == 0:
            return RouteDetail(
                ordered_path=[],
                total_distance=0,
                total_duration=0,
                step_distances=[],
                step_durations=[]
            )

        if param == "distance":
            cost_matrix: list[list[float]] = distances
        elif param == "duration":
            cost_matrix: list[list[float]] = durations
        elif param == "blended":
            cost_matrix: list[list[float]] = [[distances[i][j] + durations[i][j] for j in range(n)] for i in range(n)]
        else:
            raise ValueError("Invalid param value. Must be 'distance', 'duration', or 'blended'.")

        # Create the routing index manager
        manager = pywrapcp.RoutingIndexManager(n, 1, 0)
        routing = pywrapcp.RoutingModel(manager)

        # create distance callback
        def cost_callback(from_index: int, to_index: int) -> int:
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(round(cost_matrix[from_node][to_node]) * 1000)

        transit_callback_index = routing.RegisterTransitCallback(cost_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        search_parameters.time_limit.FromSeconds(60)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)
        if solution is None:
            raise Exception("No solution found by OR-Tools")
        # Extract the route
        index = routing.Start(0)
        route, step_distances, step_durations = [], [], []
        total_distance, total_duration = 0.0, 0.0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            next_index = solution.Value(routing.NextVar(index))
            if not routing.IsEnd(next_index):
                next_node_index = manager.IndexToNode(next_index)
                d = distances[node_index][next_node_index]
                t = durations[node_index][next_node_index]
                step_distances.append(d)
                step_durations.append(t)
                total_distance += d
                total_duration += t
            index = next_index

        if return_to_start:
            route.append(0)
            step_distances.append(distances[route[-2]][0])
            step_durations.append(durations[route[-2]][0])
            total_distance += distances[route[-2]][0]
            total_duration += durations[route[-2]][0]

        ordered_path = [locations[i] for i in route]

        return RouteDetail(
            total_distance=total_distance,
            total_duration=total_duration,
            step_distances=step_distances,
            step_durations=step_durations,
            ordered_path=ordered_path
        )