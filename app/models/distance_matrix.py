from typing import List

from pydantic import BaseModel, Field

from app.models.location import Location


class DistanceMatrix(BaseModel):
    distances: List[List[float]] = Field(..., description="2D distance matrix in meters")
    durations: List[List[float]] = Field(..., description="2D duration matrix in seconds")
    snapped_locations: List[Location] = Field(..., description="List of snapped locations")