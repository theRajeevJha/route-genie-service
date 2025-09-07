import math
from itertools import combinations
from app.models.location import Location
from app.models.route_response import RouteDetail
from app.services.shortestpath_calc import ShortestPathCalculator

class HeldKarpTspSolver(ShortestPathCalculator):

    def compute_path(self, distances:list[list[float]], durations:list[list[float]], locations:list[Location], param:str, return_to_start:bool) -> RouteDetail:
        n = len(distances)
        if n == 0:
            return RouteDetail(
                total_distance=0.0,
                total_duration=0.0,
                step_distances=[],
                step_durations=[],
                ordered_path=[]
            )

        # Choose metric
        if param == "distance":
            selection_matrix = distances
        elif param == "duration":
            selection_matrix = durations
        elif param == "blended":
            selection_matrix = [[(distances[i][j] + durations[i][j]) / 2 for j in range(n)] for i in range(n)]
        else:
            raise ValueError(f"Unknown param: {param}")

        # Held-Karp DP
        dp = {}
        for k in range(1, n):
            dp[(1 << k, k)] = (selection_matrix[0][k], 0)

        for subset_size in range(2, n):
            for subset in combinations(range(1, n), subset_size):
                bits = 0
                for bit in subset:
                    bits |= 1 << bit
                for k in subset:
                    prev_bits = bits & ~(1 << k)
                    best_cost, parent = math.inf, -1
                    for m in subset:
                        if m == k:
                            continue
                        cost = dp[(prev_bits, m)][0] + selection_matrix[m][k]
                        if cost < best_cost:
                            best_cost, parent = cost, m
                    dp[(bits, k)] = (best_cost, parent)

        bits = (1 << n) - 2  # all except start
        best_cost, last_node = math.inf, -1
        for k in range(1, n):
            cost = dp[(bits, k)][0] + (selection_matrix[k][0] if return_to_start else 0)
            if cost < best_cost:
                best_cost, last_node = cost, k

        # Reconstruct path
        path = []
        mask, k = bits, last_node
        while k != 0:
            path.append(k)
            _, parent = dp[(mask, k)]
            mask &= ~(1 << k)
            k = parent

        path.append(0)  # start
        path.reverse()  # correct order
        if return_to_start:
            path.append(0)  # return to start

        # Calculate distances & durations
        stepped_distances, stepped_durations = [], []
        total_distances, total_durations = 0, 0
        for i in range(len(path) - 1):
            d = distances[path[i]][path[i + 1]]
            t = durations[path[i]][path[i + 1]]
            stepped_distances.append(d)
            stepped_durations.append(t)
            total_distances += d
            total_durations += t

        return RouteDetail(
            total_distance=total_distances,
            total_duration=total_durations,
            step_distances=stepped_distances,
            step_durations=stepped_durations,
            ordered_path=[locations[i] for i in path]
        )