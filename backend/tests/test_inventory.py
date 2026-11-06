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
