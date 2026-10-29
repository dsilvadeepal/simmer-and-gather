"""Derived readiness: review approval is not a substitute for complete task data."""
def readiness(recipe):
    return {
        'ingredients': bool(recipe.ingredients) and bool(recipe.servings),
        'steps': bool(recipe.tasks) and all(t.evidence for t in recipe.tasks),
        'timing': bool(recipe.tasks) and all(t.minutes is not None for t in recipe.tasks),
        'same_day': bool(recipe.tasks) and all(t.preparation_policy=='same_day' or t.max_ahead_hours is not None or t.phase=='cleanup' for t in recipe.tasks),
        'advance_preparation': bool(recipe.tasks) and all(t.max_ahead_hours is not None for t in recipe.tasks if t.phase!='cleanup'),
    }

def changed_recipes(inputs,library):
    by_id={r.id:r for r in library}
    return [s.title for s in inputs.selections if s.recipe and s.recipe.id in by_id and s.recipe.version!=by_id[s.recipe.id].version]
