from pydantic import BaseModel, Field
from typing import List
from app.models.location import Location
from app.models.common import TransportMode

class RouteDetail(BaseModel):
    total_distance: float = Field(0.0, description="Total distance of the route in meters")
    total_duration: float = Field(0.0, description="Total estimated duration of the route in seconds")
    step_distances: List[float] = Field([], description="List of distances for each step in meters")
    step_durations: List[float] = Field([], description="List of durations for each step in seconds")
    ordered_path: List[Location] = Field([], description="Ordered list of route waypoints")

class RouteGroup(BaseModel):
    shortest_duration: RouteDetail = Field(..., description="route computed based on shortest duration")
    shortest_distance: RouteDetail = Field(..., description="route computed based on shortest distance")
    shortest_blended: RouteDetail = Field(..., description="route computed based on blended metric based on both distance and duration")

class RouteResponse(BaseModel):
    route_groups: List[RouteGroup] = Field(..., description="List of route groups")
    mode: TransportMode = Field( ..., description="Mode of transportation")
    start_location: Location = Field(..., description="Starting point of the route")
