import pytest
from simmer.menu import recommend_counts, propose_menu, validate_menu
from simmer.domain import *

def test_thanksgiving_counts_are_adjustable_not_fixed_two_mains():
    g=Gathering(occasion='Thanksgiving',spread='generous')
    assert recommend_counts(g)['sides']>2
    g.category_counts={'mains':4}
    assert recommend_counts(g)['mains']==4

def test_proposal_preserves_must_have_and_uses_saved_recipes_first():
    must=MenuSelection(id='keep',title='Family favorite',must_have=True,mode='buy',servings=15)
    r=RecipeSnapshot(title='Vegetarian rice',source='saved',reviewed=True,category='sides',vegetarian=True,allergens=[],servings=5)
    i=PlanInputs(gathering=Gathering(vegetarian_guests=5,allergies=[]),selections=[must])
    result=propose_menu(i,[r])
    assert result[0]==must
    assert any(s.recipe and s.recipe.id==r.id for s in result)

def test_unknown_or_insufficient_vegetarian_coverage_is_visible():
    i=PlanInputs(gathering=Gathering(vegetarian_guests=5,allergies=['peanut']),selections=[MenuSelection(title='Rice',mode='buy',servings=2,vegetarian=True)])
    assert validate_menu(i)

def test_model_suggestion_cannot_invent_recipe_ids_and_has_one_repair():
    from simmer.menu import rank_recipes
    recipes=[RecipeSnapshot(id='known',title='Rice',source='saved')]
    calls=[]
    def bad(messages): calls.append(1); return '{"recipe_ids":["invented"]}'
    assert rank_recipes(Gathering(),recipes,bad)==recipes
    assert len(calls)==2

def test_ingredient_screen_detects_peanut_even_when_nuts_declared_empty():
    r=RecipeSnapshot(title='Salad',source='test',allergens=[],ingredients=[Ingredient(name='roasted peanuts')])
    i=PlanInputs(gathering=Gathering(allergies=['nuts']),selections=[MenuSelection(title='Salad',recipe=r)])
    assert any(v.code=='allergy' and 'peanuts' in v.explanation for v in validate_menu(i))

def test_absence_of_obvious_ingredient_does_not_claim_allergy_safe():
    r=RecipeSnapshot(title='Rice',source='test',allergens=[],ingredients=[Ingredient(name='rice')])
    i=PlanInputs(gathering=Gathering(allergies=['gluten']),selections=[MenuSelection(title='Rice',recipe=r)])
    assert any(v.code=='allergy_unknown' for v in validate_menu(i))


def test_reviewed_ingredient_screen_is_reminder_not_safety_certification():
    from simmer.menu import menu_blockers
    r=RecipeSnapshot(title='Rice',source='test',reviewed=True,allergens=[],ingredients=[Ingredient(name='rice')])
    i=PlanInputs(gathering=Gathering(allergies=['nuts']),selections=[MenuSelection(title='Rice',recipe=r)])
    issues=validate_menu(i)
    assert not menu_blockers(issues)
    assert any(v.code=='allergy_label_check' and 'not an allergen-free guarantee' in v.explanation for v in issues)


@pytest.mark.parametrize('mode,reviewed,ingredients,allergens,allergy',[
    ('cook',False,['rice'],[],'nuts'),
    ('cook',True,[],[],'nuts'),
    ('cook',True,['rice'],None,'nuts'),
    ('buy',True,['rice'],[],'nuts'),
    ('cook',True,['rice'],[],'sesame'),
])
def test_insufficient_or_unsupported_screen_remains_blocking(mode,reviewed,ingredients,allergens,allergy):
    from simmer.menu import menu_blockers
    r=RecipeSnapshot(title='Rice',source='test',reviewed=reviewed,allergens=allergens,ingredients=[Ingredient(name=n) for n in ingredients])
    i=PlanInputs(gathering=Gathering(allergies=[allergy]),selections=[MenuSelection(title='Rice',mode=mode,recipe=r)])
    assert any(v.code=='allergy_unknown' for v in menu_blockers(validate_menu(i)))


def test_reviewed_recipe_with_nuts_remains_blocking():
    from simmer.menu import menu_blockers
    r=RecipeSnapshot(title='Rice',source='test',reviewed=True,allergens=[],ingredients=[Ingredient(name='cashews')])
    i=PlanInputs(gathering=Gathering(allergies=['nuts']),selections=[MenuSelection(title='Rice',recipe=r)])
    assert any(v.code=='allergy' for v in menu_blockers(validate_menu(i)))
