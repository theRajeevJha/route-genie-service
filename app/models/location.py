from pydantic import BaseModel, Field

class Location(BaseModel):
    latitude: float = Field(..., description="Latitude of the location", examples=[37.7749])
    longitude: float = Field(..., description="Longitude of the location", examples=[-122.4194])
    id: str = Field(..., description="id/name of the location", examples=["San Francisco, CA"])
    snapped_distance: float = Field(0.0, description="distance from original point to snapped point on road")