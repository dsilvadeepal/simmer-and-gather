"""Validate the curated home-cook timing draft without rewriting estimates."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
recipes=json.loads((ROOT/'docs/recipe-collection.json').read_text())
timings=json.loads((ROOT/'docs/recipe-chef-timing.json').read_text())
assert len(recipes)==len(timings)==40
assert [x['url'] for x in recipes]==[x['url'] for x in timings]
assert len({x['url'] for x in recipes})==40
for recipe,timing in zip(recipes,timings):
    assert recipe['title']==timing['title']
    assert recipe.get('ingredients'),recipe['title']
    assert timing['active_minutes']==sum(p['active_minutes'] for p in timing['phases'])+timing['cleanup_minutes'],recipe['title']
    assert timing['unattended_minutes']==sum(p['unattended_minutes'] for p in timing['phases']),recipe['title']
    assert timing['elapsed_minutes']==timing['active_minutes']+timing['unattended_minutes'],recipe['title']
print('40 recipes and timing totals validated')
