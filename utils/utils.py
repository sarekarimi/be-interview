import re
from typing import Tuple

from fastapi import HTTPException, status


def parse_bounding_box(bbox: str) -> Tuple[float, float, float, float] | None:
    """
    Parses a bounding box string in the format "min_lat,min_lon,max_lat,max_lon".
    """
    if not bbox:
        return None

    # Remove whitespace and check format
    bbox = bbox.replace(' ', '')
    match = re.match(r'([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+)', bbox)

    if not match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bounding box must be in format: min_lat,min_lon,max_lat,max_lon")

    min_lat, min_lon, max_lat, max_lon = map(float, match.groups())

    # Validate coordinates
    if not (-180 <= min_lon <= 180 and -180 <= max_lon <= 180):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Longitude must be between -180 and 180")
    if not (-90 <= min_lat <= 90 and -90 <= max_lat <= 90):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Latitude must be between -90 and 90")
    if max_lon <= min_lon:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="max_lon must be greater than min_lon")
    if max_lat <= min_lat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="max_lat must be greater than min_lat")

    return min_lat, min_lon, max_lat, max_lon
