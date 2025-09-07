import json
from typing import List
import httpx
import time
from loguru import logger

from app.core.config import ORS_API_KEY
from app.models.distance_matrix import DistanceMatrix
from app.models.location import Location
from app.models.route_request import RouteRequest
from app.models.common import TransportMode
from app.services.distance_provider import DistanceProvider


def parse_ors_response(ors_response: dict, destinations:List[Location], start:Location) -> DistanceMatrix:
    """
    Parse the OpenRouteService response to extract distance and duration matrices.
    Assign original location id to snapped locations.
    """
    ors_locations = ors_response.get("destinations", [])
    # add start location first
    locations = [Location(
        id=start.id,
        latitude=ors_locations[0]["location"][1],
        longitude=ors_locations[0]["location"][0],
        snapped_distance=ors_locations[0].get("snapped_distance", 0.0)
    )]

    # add other locations
    for idx, loc in enumerate(destinations, start=1):
        ors_loc = ors_locations[idx]
        locations.append(Location(
            id=loc.id,
            latitude=ors_loc["location"][1],
            longitude=ors_loc["location"][0],
            snapped_distance=ors_loc.get("snapped_distance", 0.0)
        ))
    return DistanceMatrix(
        distances=ors_response.get("distances"),
        durations=ors_response.get("durations"),
        snapped_locations=locations
    )



class OpenRouteServiceDistanceProvider(DistanceProvider):
    """Distance provider using OpenRouteService Matrix API."""

    def __init__(self):
        self.api_key = ORS_API_KEY
        self.base_url = "https://api.openrouteservice.org/v2/matrix/"

    async def get_distance_matrix(self, route_req: RouteRequest) -> DistanceMatrix:
        """
        Build profile, prepare payload and fetch distance matrix from ORS.
        """
        profile = "driving-car"
        if route_req.mode == TransportMode.TRUCK:
            profile = "foot-walking"
        elif route_req.mode == TransportMode.BIKE:
            profile = "cycling-regular"

        full_url = self.base_url + profile
        logger.info(f"Fetching distance matrix from ORS profile={profile} url={full_url}")

        return await self._fetch_distance_matrix(full_url, route_req)

    async def _fetch_distance_matrix(self, url: str, route_req: RouteRequest) -> DistanceMatrix:
        coordinates = [[route_req.start.longitude, route_req.start.latitude]] + [
            [loc.longitude, loc.latitude] for loc in route_req.routes
        ]

        payload = {
            "locations": coordinates,
            "metrics": ["distance", "duration"],
            "units": "m",
        }
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json; charset=utf-8",
        }

        logger.debug(f"ORS distance matrix request payload: {json.dumps(payload, indent=2)}")

        start_time = time.time()
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)

        elapsed = time.time() - start_time
        logger.info(f"ORS response status={response.status_code} in {elapsed:.2f}s")

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"ORS API error: {e.response.text}")
            raise

        data = response.json()
        logger.debug(f"ORS distance matrix response: {json.dumps(data, indent=2)}")
        return parse_ors_response(data, route_req.routes, route_req.start)
