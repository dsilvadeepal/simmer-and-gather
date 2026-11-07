"""Regression gates for the second evaluation batch's three real failures."""
import json
from pathlib import Path
from simmer.domain import PlanInputs
from simmer.menu import validate_menu,menu_blockers
from simmer.scheduler import schedule,validate_schedule
ROOT=Path(__file__).resolve().parents[2]
CASES=json.loads((ROOT/'evals/heldout-gatherings-corrected.json').read_text())

def test_short_helper_case_keeps_preferences_and_passes_independent_validator():
 data=PlanInputs.model_validate(CASES[10]['inputs']);before=data.model_dump(mode='json')
 result=schedule(data)
 assert result.outcome.code=='complete'
 assert not validate_schedule(data,result)
 assert data.model_dump(mode='json')==before

def test_corrected_dietary_screening_keeps_gluten_restriction_and_label_reminders():
 data=PlanInputs.model_validate(CASES[13]['inputs'])
 assert data.gathering.allergies==['gluten']
 issues=validate_menu(data)
 assert not menu_blockers(issues)
 assert sum(v.code=='allergy_label_check' for v in issues)==3
 for s in data.selections[:2]:
  assert 'milk' in s.recipe.allergens
  assert 'allergen_review' in s.recipe.preparation_provenance
 # A dairy request must still block the ghee recipes.
 data.gathering.allergies=['milk']
 assert any(v.code=='allergy' for v in validate_menu(data))

def test_known_conflicts_remain_blocking():
 for index in (15,16,17):
  assert menu_blockers(validate_menu(PlanInputs.model_validate(CASES[index]['inputs'])))
