from simmer.adapters.notion_recipe_details import ingredient

def test_whole_food_counts_import_as_scalable_amounts():
    for line,quantity in [('1 lemon (juiced)',1),('15 raw cashews (**)',15),('12 black peppercorns',12),('3 green cardamom pods',3),('10 carrots (peeled and grated)',10)]:
        row=ingredient(line)
        assert row.quantity==quantity
        assert row.unit=='count'

def test_ranges_and_unknown_units_are_not_guessed():
    assert ingredient('1 to 2 teaspoon hot green chili').quantity is None
    assert ingredient('2 handfuls spinach').quantity is None

def test_published_count_round_trip():
    row=ingredient('15 count raw cashews (**)')
    assert row.quantity==15 and row.unit=='count' and row.name=='raw cashews (**)'
