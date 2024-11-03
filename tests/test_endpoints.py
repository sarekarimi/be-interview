from pathlib import Path
from typing import Generator
from unittest.mock import patch
from uuid import uuid4
from fastapi import status
import alembic.command
import alembic.config
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.db import get_database_session
from app.main import app
from app.models import Organisation

_ALEMBIC_INI_PATH = Path(__file__).parent.parent / "alembic.ini"


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def apply_alembic_migrations() -> Generator[None, None, None]:
    # Creates test database per test function
    test_db_file_name = f"test_{uuid4()}.db"
    database_path = Path(test_db_file_name)
    try:
        test_db_url = f"sqlite:///{test_db_file_name}"
        alembic_cfg = alembic.config.Config(_ALEMBIC_INI_PATH)
        alembic_cfg.attributes["sqlalchemy_url"] = test_db_url
        alembic.command.upgrade(alembic_cfg, "head")
        test_engine = create_engine(test_db_url, echo=True)
        with patch("app.db.get_engine") as mock_engine:
            mock_engine.return_value = test_engine
            yield
        test_engine.dispose()
    finally:
        database_path.unlink(missing_ok=True)


def test_organisation_endpoints(test_client: TestClient) -> None:
    list_of_organisation_names_to_create = ["organisation_a", "organisation_b", "organisation_c"]

    # Validate that organisations do not exist in database
    with get_database_session() as database_session:
        organisations_before = database_session.query(Organisation).all()
        database_session.expunge_all()
    assert len(organisations_before) == 0

    # Create organisations
    for organisation_name in list_of_organisation_names_to_create:
        response = test_client.post("/api/organisations/create", json={"name": organisation_name})
        assert response.status_code == status.HTTP_200_OK

    # Validate that organisations exist in database
    with get_database_session() as database_session:
        organisations_after = database_session.query(Organisation).all()
        database_session.expunge_all()
    created_organisation_names = set(organisation.name for organisation in organisations_after)
    assert created_organisation_names == set(list_of_organisation_names_to_create)

    # Validate that created organisation by id can be retried via API
    with get_database_session() as database_session:
        organisation = database_session.query(Organisation).filter(Organisation.id == organisations_after[0].id).first()
        database_session.expunge_all()
    assert organisation.id == 1

    # Validate that created organisations can be retried via API
    response = test_client.get("/api/organisations")
    organisations = set(organisation["name"] for organisation in response.json())
    assert set(organisations) == created_organisation_names

    # Create location
    response = test_client.post("/api/organisations/create/location",
                                json={"organisation_id": 1, "location_name": "Vienna",
                                      "latitude": 40.5, "longitude": -13.5})
    assert response.status_code == status.HTTP_200_OK

    # Validate that location exist in database without bounding_box
    response = test_client.get("api/organisations/1/locations")
    assert response.status_code == 200
    locations = response.json()
    assert len(locations) == 1  # One location should be returned

    # Validate that location exist in database with bounding_box
    bounding_box = "-14.0,-20.0,50.0,41.0"
    response = test_client.get(f"api/organisations/1/locations?bounding_box={bounding_box}")
    assert response.status_code == 200
    locations = response.json()
    assert len(locations) == 1

