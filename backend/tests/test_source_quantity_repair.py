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

def test_ounces_and_exact_whole_eggs_are_parsed():
    assert ingredient('12 ounces fresh cranberries').quantity == 12
    assert ingredient('12 ounces fresh cranberries').unit == 'oz'
    assert ingredient('2 large eggs').quantity == 2

def test_specific_extra_counts_and_zest_do_not_guess_ranges():
    assert ingredient('8 Naan').quantity==8
    assert ingredient('zest of 1 orange').quantity==1
    assert ingredient('12 fresh basil leaves').quantity==12
    assert ingredient('1-2 tbsp oil').quantity is None

def test_explicit_source_units_and_ranges_are_not_confused():
    assert ingredient('1 kilo boneless pork').unit=='kg'
    assert ingredient('1 pinch saffron').unit=='pinch'
    assert ingredient('12 Kashmiri chillies, deseeded').quantity==12
    assert ingredient('2  medium sized onions').quantity==2
    assert ingredient('1-2 tbsp oil').quantity is None

def test_source_singular_inches_and_exact_fruit_counts():
    assert ingredient('1 inch fresh ginger, minced').unit=='inch'
    assert ingredient('1 Granny smith apple (diced)').quantity==1
    assert ingredient('1 bottle of dry white wine').quantity==1
    assert ingredient('1 to 2 teaspoons chili powder').quantity is None

def test_source_typography_inches_and_mixed_fraction():
    r=ingredient('2″ cinnamon')
    assert r.quantity==2 and r.unit=='inch'
    r=ingredient('1 & 1/2 inch piece of ginger')
    assert r.quantity==1.5 and r.unit=='inch'

def test_source_count_with_explicit_measured_equivalent():
    r=ingredient('½ (1 cup) Medium Red Onion, finely diced')
    assert r.quantity==1 and r.unit=='cup' and 'Onion' in r.name
    r=ingredient('½ (½ cup) Medium Tomato')
    assert r.quantity==.5 and r.unit=='cup'

def test_package_counts_preserve_package_size():
    row=ingredient('1 (8-ounce) brie cheese round (cold)')
    assert row.quantity==1 and row.unit=='count' and '8-ounce' in row.name
    row=ingredient('1 9-inch pie crust')
    assert row.quantity==1 and row.unit=='count' and '9-inch' in row.name
