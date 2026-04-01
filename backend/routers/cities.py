from fastapi import APIRouter, HTTPException, Query, status

from backend.schemas.city import CityResult
from backend.services.geocoding import GeocodingError, search_city


router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/search", response_model=list[CityResult])
async def search_cities(
    q: str = Query(min_length=2, max_length=100),
    limit: int = Query(default=5, ge=1, le=10),
) -> list[CityResult]:
    try:
        return await search_city(q, limit)
    except GeocodingError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc