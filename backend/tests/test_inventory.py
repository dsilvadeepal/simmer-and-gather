import pytest
from simmer.domain import *
from simmer.inventory import shopping_for, confirm_items

def test_only_confirmed_stock_deducts_compatible_units():
    r=RecipeSnapshot(title='Rice',source='test',servings=4,ingredients=[Ingredient(name='rice',quantity=1,unit='kg')])
    inputs=PlanInputs(gathering=Gathering(),selections=[MenuSelection(title='Rice',recipe=r,servings=8)],inventory=[InventoryItem(name='rice',quantity=500,unit='g',confirmed=True)])
    assert shopping_for(inputs)[0].quantity==1.5
    inputs.inventory[0].confirmed=False
    assert shopping_for(inputs)[0].quantity==2
    inputs.inventory[0].confirmed=True; inputs.inventory[0].unit='cup'
    assert shopping_for(inputs)[0].quantity==2

def test_duplicate_inventory_requires_review():
    with pytest.raises(ValueError): confirm_items([InventoryItem(name='rice',quantity=1,unit='kg'),InventoryItem(name='Rice',quantity=1,unit='kg')])

def test_guest_items_excluded_bought_items_included():
    i=PlanInputs(gathering=Gathering(),selections=[MenuSelection(title='Cake',mode='guest',servings=10),MenuSelection(title='Samosas',mode='buy',servings=15)])
    assert [x.name for x in shopping_for(i)]==['Samosas']

def test_clean_names_combine_without_losing_unknown_amounts():
    r=RecipeSnapshot(title='Vegetables',source='test',servings=4,ingredients=[Ingredient(name='cumin seeds (crushed)',quantity=1,unit='tsp'),Ingredient(name='cumin seeds',quantity=2,unit='tsp'),Ingredient(name='water',quantity=1,unit='cup'),Ingredient(name='6 cloves',quantity=6,unit='count'),Ingredient(name='cloves',quantity=None,unit='count')])
    i=PlanInputs(gathering=Gathering(),selections=[MenuSelection(title='Vegetables',recipe=r,servings=8)])
    rows={x.name:x for x in shopping_for(i)}
    assert rows['cumin seeds'].quantity==6
    assert rows['cloves'].quantity is None
    assert 'water' not in rows

def test_embedded_count_is_scaled_but_ranges_remain_unresolved():
    r=RecipeSnapshot(title='Curry',source='test',servings=4,ingredients=[Ingredient(name='1 large yellow onion (chopped)'),Ingredient(name='1 to 2 tsp pepper')])
    i=PlanInputs(gathering=Gathering(),selections=[MenuSelection(title='Curry',recipe=r,servings=8)])
    rows=shopping_for(i)
    assert rows[0].quantity==2 and rows[0].unit=='count'
    assert rows[1].quantity is None

def test_unspecified_range_retains_source_words_for_shopping_review():
    r=RecipeSnapshot(title='Curry',source='test',servings=4,ingredients=[Ingredient(name='1 to 2 tsp pepper (to taste)')])
    i=PlanInputs(gathering=Gathering(),selections=[MenuSelection(title='Curry',recipe=r,servings=8)])
    item=shopping_for(i)[0]
    assert item.quantity is None
    assert item.amount_detail.source_text=='1 to 2 tsp pepper (to taste)'
    assert (item.amount_detail.minimum,item.amount_detail.maximum)==(2,4)

def test_source_range_is_scaled_without_claiming_exact_amount():
    r=RecipeSnapshot(title='Curry',source='test',servings=4,ingredients=[Ingredient(name='1 to 2 teaspoons chili powder')])
    i=PlanInputs(gathering=Gathering(),selections=[MenuSelection(title='Curry',recipe=r,servings=8)])
    row=shopping_for(i)[0]
    assert row.quantity is None
    assert 'scaled range: 2–4 teaspoons' in row.name

def test_alternative_ingredients_are_not_falsely_treated_as_one_unit():
    from simmer.inventory import scaled_range_note
    assert scaled_range_note('4 to 8 small green chiles (or 1 to 2 jalapeños)',2).startswith('4 to 8 small')

def test_range_scaling_handles_counts_and_mixed_unicode_fractions():
    from simmer.inventory import scaled_range_note
    assert '6–8 large onions' in scaled_range_note('3-4 large onions',2)
    assert '3–4 cups' in scaled_range_note('1½ -2 cups bread crumbs',2)
    original='4 to 8 small green chiles (or 1 to 2 jalapeños)'
    assert scaled_range_note(original,2)==original

def test_shopping_retains_package_size():
    r=RecipeSnapshot(title='Brie',source='test',servings=4,ingredients=[Ingredient(name='1 (8-ounce) brie cheese round (cold)')])
    i=PlanInputs(gathering=Gathering(),selections=[MenuSelection(title='Brie',recipe=r,servings=8)])
    row=shopping_for(i)[0]
    assert row.quantity==2 and '(8-ounce)' in row.name
