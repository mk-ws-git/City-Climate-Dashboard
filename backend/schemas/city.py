from pydantic import BaseModel


class CityResult(BaseModel):
    name: str
    country: str | None = None
    latitude: float
    longitude: float
    mapbox_id: str | None = None
    bbox: list[float] | None = None