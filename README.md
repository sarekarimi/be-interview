# Junior Backend Developer Take-Home Assignment

Welcome! This assignment is designed to assess your skills in writing clean code, code
review, implementing features, and testing.

Feel free to make any changes to this repository if you believe they’re necessary.

Please work through the tasks and send us a link to your forked repository within the
next 72 hours. If any questions arise, don't hesitate to reach out to us.

This is a junior position, and we understand if you cannot complete all tasks - spending
more than 2 hours on this assignment is not expected. Simply send us what you accomplish
within that time.

## Getting Started

- Fork this repository to your own GitHub account.
- Ensure you have Python 3.10+ installed.
- Install dependencies using `pip install -r requirements.txt`.
- Run `python -m alembic upgrade head` to set up the database.
- Run the FastAPI server using `python -m uvicorn app.main:app --reload`.
- Open `http://localhost:8000/docs` in your browser to see the API documentation and to
  test it.
- For running tests use `python -m pytest`.

## Tasks

### Task 1: Implement missing endpoint

Endpoint `GET /organisation/create/location` is missing implementation. Please implement
this endpoint for creating locations.

### Task 2: Code smells

Endpoint `GET /organisation/{organisation_id}/locations` is not looking nicely.
Please fix it so that it will look more like production ready code.

### Task 3: Query by location

There is a new requirement that the endpoint
`GET /organisation/{organisation_id}/locations` should take an optional parameter called
`bounding_box` (tuple of 4 bounding coordinates) and should return only the locations
that are completely within the bounding box.

### Task 4: Code formating

If you feel like that the code could look nicer and more readable please refactor it.

### Task 5 (Bonus): Add tests

Please add missing tests so that every endpoint is tested.
