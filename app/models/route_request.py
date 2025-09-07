from pydantic import BaseModel, Field
from typing import List
from app.models.location import Location
from app.models.common import TransportMode

class RouteRequest(BaseModel):
    mode: TransportMode = Field( ..., description="Mode of transportation")
    start: Location = Field(..., description="Starting point of the route")
    routes: List[Location] = Field(..., description="List of route waypoints")

