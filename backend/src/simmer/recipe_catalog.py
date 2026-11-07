"""Curated method/timing review; source-supported storage is kept as guidance."""
import json
from pathlib import Path

def reviewed_recipe(source):
    rows=json.loads((Path(__file__).parent/'data'/'reviewed_recipes.json').read_text())
    return next((r for r in rows if r['url'].rstrip('/')==source.rstrip('/')),None)
