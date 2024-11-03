from sqlmodel import SQLModel, Field, Relationship


class Base(SQLModel):
    pass


class CreateOrganisation(Base):
    name: str


class Organisation(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    locations: list["Location"] = Relationship(back_populates="organisation")


class CreateLocationResponse(Base):
    location_name: str
    longitude: float
    latitude: float


class CreateLocation(Base):
    organisation_id: int = Field(foreign_key="organisation.id")
    location_name: str
    latitude: float
    longitude: float


class Location(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    organisation_id: int = Field(default=None, foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="locations")
    location_name: str
    longitude: float
    latitude: float
