import httpx

from backend.core.config import settings
from backend.schemas.city import CityResult


class GeocodingError(Exception):
    pass


async def search_city(query: str, limit: int = 5) -> list[CityResult]:
    token = settings.mapbox_access_token
    if not token:
        raise GeocodingError("MAPBOX_ACCESS_TOKEN is not configured")

    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json"
    params = {
        "access_token": token,
        "types": "place",
        "limit": max(1, min(limit, 10)),
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, params=params)

    if resp.status_code != 200:
        raise GeocodingError(f"Mapbox geocoding failed: {resp.status_code}")

    data = resp.json()
    features = data.get("features", [])

    results: list[CityResult] = []
    for f in features:
        center = f.get("center") or [None, None]
        lon, lat = center[0], center[1]
        if lat is None or lon is None:
            continue

        context = f.get("context", [])
        country = None
        for c in context:
            if "country" in (c.get("id") or ""):
                country = c.get("text")
                break

        results.append(
            CityResult(
                name=f.get("text", ""),
                country=country,
                latitude=float(lat),
                longitude=float(lon),
                mapbox_id=f.get("id"),
                bbox=f.get("bbox"),
            )
        )

    return results