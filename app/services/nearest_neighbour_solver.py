from app.models.location import Location
from app.models.route_response import RouteDetail
from app.services.shortestpath_calc import ShortestPathCalculator

class NearestNeighbourRoute(ShortestPathCalculator):

    def compute_path(self, distance_matrix: list[list[float]], duration_matrix: list[list[float]], locations: list[Location], route_type: str, return_to_start: bool) -> RouteDetail:
        n = len(locations)
        if n == 0:
            return RouteDetail(
                total_distance=0.0,
                total_duration=0.0,
                step_distances=[],
                step_durations=[],
                ordered_path=[]
            )
        if route_type == "distance":
            selection_matrix = distance_matrix
        elif route_type == "duration":
            selection_matrix = duration_matrix
        elif route_type == "blended":
            selection_matrix = [[(distance_matrix[i][j] + duration_matrix[i][j]) / 2 for j in range(n)] for i in
                                range(n)]
        else:
            raise ValueError(f"Unknown route_type: {route_type}")

        visited: list[bool] = [False] * n
        current = 0
        route_indices = [current]
        visited[current] = True
        step_distances = []
        step_durations = []
        while len(route_indices) < n:
            nearest_dist = float("inf")
            nearest_index = None
            for i in range(n):
                if not visited[i] and selection_matrix[current][i] < nearest_dist:
                    nearest_dist = selection_matrix[current][i]
                    nearest_index = i
            if nearest_index is None:
                break
            visited[nearest_index] = True
            route_indices.append(nearest_index)

            step_distances.append(distance_matrix[current][nearest_index])
            step_durations.append(duration_matrix[current][nearest_index])
            current = nearest_index

        if return_to_start and len(route_indices) > 1:
            start_index = route_indices[0]
            step_distances.append(distance_matrix[current][start_index])
            step_durations.append(duration_matrix[current][start_index])
            route_indices.append(start_index)
        ordered_path = [locations[i] for i in route_indices]
        total_distance = sum(step_distances)
        total_duration = sum(step_durations)

        return RouteDetail(
            total_distance=total_distance,
            total_duration=total_duration,
            step_distances=step_distances,
            step_durations=step_distances,
            ordered_path=ordered_path
        )
