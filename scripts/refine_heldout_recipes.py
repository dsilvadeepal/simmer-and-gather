"""Narrow, source-reviewed metadata corrections; never infer allergen-free status."""
SOURCES={
 'https://ministryofcurry.com/instant-pot-butter-chicken',
 'https://ministryofcurry.com/instant-pot-chana-masala-recipe',
 'https://ministryofcurry.com/tandoori-chicken-wings',
 'https://www.wellplated.com/garlic-mashed-potatoes',
}
def refine(recipe):
 r=recipe.model_copy(deep=True)
 if r.source.rstrip('/') not in SOURCES:return r
 # Ghee is listed, with an oil alternative. Preserve the dairy warning.
 # No wheat/barley/rye or nut ingredients in these reviewed curry ingredient lists.
 from simmer.menu import ingredient_allergen_hits
 hits=ingredient_allergen_hits(r,{'nuts','gluten'})
 if not r.reviewed or not r.ingredients or hits:raise ValueError('Ingredient list changed; re-review '+r.title)
 r.allergens=sorted(set(r.allergens or [])|{'milk'})
 r.preparation_provenance['allergen_review']='2026-11-07: saved ingredients reviewed against '+r.source+'. Milk ingredients are listed (ghee, yogurt, milk, cream or butter depending on recipe). No nuts or gluten detected in this recipe ingredient list. Check packaged ingredients including spice blends and pastes, and prevent cross-contact. Accompaniments and optional substitutions require separate checks. Not an allergen-free certification.'
 return r
