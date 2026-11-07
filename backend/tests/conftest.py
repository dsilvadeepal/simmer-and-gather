import os
from uuid import uuid4
import pytest

@pytest.fixture
def owner(): return str(uuid4())

@pytest.fixture
def store():
    from simmer.db import Store
    s = Store(os.getenv('TEST_DATABASE_URL', 'postgresql+psycopg://simmer:local-dev-only@localhost:55444/simmer'))
    s.create_schema()
    return s
