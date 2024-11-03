from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlmodel import select, Session

from app.db import get_db
from app.models import Location, Organisation, CreateLocationResponse, CreateOrganisation, CreateLocation
from utils.utils import parse_bounding_box

router = APIRouter()


@router.post("/create", response_model=Organisation)
def create_organisation(create_organisation: CreateOrganisation, session: Session = Depends(get_db)) -> Organisation:
    """
    Create an organisation.
    """
    organisation = Organisation(name=create_organisation.name)
    session.add(organisation)
    session.commit()
    session.refresh(organisation)
    return organisation


@router.get("/", response_model=list[Organisation])
def get_organisations(session: Session = Depends(get_db)) -> list[Organisation]:
    """
    Get all organisations.
    """
    organisations = session.exec(select(Organisation)).all()
    return organisations


@router.get("/{organisation_id}", response_model=Organisation)
def get_organisation(organisation_id: int, session: Session = Depends(get_db)) -> Organisation:
    """
    Get an organisation by id.
    """
    organisation = session.get(Organisation, organisation_id)
    if organisation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    return organisation


@router.post("/create/location", response_model=CreateLocationResponse)
def create_location(create_location: CreateLocation, session: Session = Depends(get_db)) -> Location:
    """
    Create a location associated with an organisation.
    """
    organisation = session.exec(select(Organisation).where(Organisation.id == create_location.organisation_id)).first()
    if organisation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organisation not found."
        )

    location = Location(**create_location.dict())
    session.add(location)
    session.commit()
    session.refresh(location)
    return location


@router.get("/{organisation_id}/locations", response_model=list[CreateLocationResponse])
def get_organisation_locations(organisation_id: int,
                               bounding_box: Optional[str] = Query(
                                   None,
                                   description="Bounding box: min_lat, min_lon, max_lat, max_lon",
                                   example="-74.0,40.0,-73.0,41.0",
                                   regex=r"^[-\d.]+,[-\d.]+,[-\d.]+,[-\d.]+$"
                               ),
                               session: Session = Depends(get_db)):
    """
    Get list of locations for an organisation with optional bounding box filter.
    """
    locations_query = select(Location).where(Location.organisation_id == organisation_id)

    # Apply bounding box filter if provided
    if bounding_box:
        min_lat, min_lon, max_lat, max_lon = parse_bounding_box(bounding_box)
        locations_query = (
            select(Location)
            .where(Location.latitude.between(min_lat, max_lat))
            .where(Location.longitude.between(min_lon, max_lon))
        )
    locations = session.exec(locations_query).all()

    return locations
