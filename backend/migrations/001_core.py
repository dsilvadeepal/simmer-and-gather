"""Initial document store. Apply via `uv run python backend/migrations/001_core.py`."""
import os
from simmer.db import Store
if __name__ == '__main__': Store(os.environ['DATABASE_URL']).create_schema()
