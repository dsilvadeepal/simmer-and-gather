from simmer.adapters.notion_recipe_details import notion_cover
from simmer.adapters.notion_client import candidate_from_page

def test_cover_is_imported_into_recipe():
    page={'id':'recipe','cover':{'type':'external','external':{'url':'https://example.org/dish.jpg'}},'properties':{}}
    assert candidate_from_page(page).image_url=='https://example.org/dish.jpg'
    assert notion_cover({'cover':None}) is None
