"""Source-grounded Christmas task proposals; minutes are planning allowances.

No I/O on import. Caller owns versioned saves and gathering-specific windows.
"""
from simmer.domain import PrepTask, AttentionSegment, Ingredient

def step(id,title,minutes,guidance,*,deps=(),active=None,resource=None,ahead=72,segments=None,anchor='serving'):
    active=minutes if active is None else active
    return PrepTask(id=id,title=title,minutes=minutes,active_minutes=active,presence_minutes=active,
        dependencies=list(deps),resource=resource,max_ahead_hours=ahead,
        preparation_policy='advance' if ahead is not None else 'same_day',storage_anchor=anchor,
        attention_segments=[AttentionSegment(offset_minutes=a,minutes=b) for a,b in (segments or [])],
        unattended=active==0,scale_mode='combined',guidance=guidance,
        evidence='Publisher method; task minutes and check-in placement are planning estimates. '+('Same-day preparation.' if ahead is None else 'Make-ahead allowance is a planning estimate; follow storage notes.'),timing_basis='estimate')

def refine(recipe):
    r=recipe.model_copy(deep=True)
    if 'Vindaloo' in r.title:
        r.tasks=[
          step('prepare','Cut pork, blend spice paste and chop onions',30,'Cut pork into even pieces. Blend the spices with vinegar; chop the onions.' ,ahead=48),
          step('cook','Cook the vindaloo until the pork is tender',105,'Soften onions, fry the spice paste, then coat the pork. Add water and simmer covered; check liquid and tenderness. Cool promptly in shallow containers and refrigerate.',deps=['prepare'],active=40,resource='stovetop',ahead=48,segments=[(0,25),(45,5),(75,5),(100,5)]),
          step('reheat','Reheat vindaloo',30,'Reheat until piping hot throughout, stirring and adding a splash of water if needed. Keep hot until serving.',deps=['cook'],active=10,resource='stovetop',ahead=None,segments=[(0,5),(25,5)])]
    elif 'Cafreal' in r.title:
        r.tasks=[
          step('paste','Prepare chicken and blend cafreal paste',35,'Score chicken and season with lemon, ginger, garlic and salt. Blend the green paste. Coat chicken with half; keep the unused paste separately covered in the fridge.',ahead=24),
          step('marinate','Refrigerate chicken in its marinade',180,'Leave covered in the fridge for at least 2–3 hours, or overnight. Keep reserved paste separate from raw chicken.',deps=['paste'],active=0,ahead=24),
          step('cook','Sear chicken, then cook in cafreal paste',45,'Brown both sides in butter and oil. Add reserved paste and a little water; cover and cook, then uncover to reduce the sauce. Check the thickest pieces are cooked through.',deps=['marinate'],active=25,resource='stovetop',ahead=None,segments=[(0,15),(25,5),(40,5)])]
    elif 'Caldin' in r.title:
        r.tasks=[
          step('base','Blend coconut extract and cook the caldin base',50,'Grind spices, ginger, garlic, chilli and coconut with water; strain, then extract a second time. Soften onion and tomato. Add the extract, tamarind and seasoning; simmer gently.',resource='stovetop',ahead=None),
          step('fish','Season fish and finish the caldin',20,'Season fish with salt and turmeric. Gently cook it in the simmering curry; add chilli and coconut cream toward the end. Stop when the fish is opaque and flakes easily.',deps=['base'],resource='stovetop',ahead=None)]
    elif 'Sannas' in r.title:
        # A distinct, complete source variant; never mix yeast quantities with toddy instructions.
        r.title='Goan Sannas (yeast method)'
        r.source='https://xantilicious.com/recipe/sanna/'
        r.servings=10  # 18–20 pieces, estimated two per buffet portion.
        r.ingredients=[Ingredient(name=n,quantity=q,unit=u) for n,q,u in [('Parboiled rice',2,'cups'),('Grated coconut',.5,'cup'),('Sugar',3,'tbsp'),('Yeast',1,'tsp'),('Salt',1,'tsp'),('Coconut water or water',None,None),('Oil for molds',None,None)]]
        r.source_text='Xantilicious yeast sannas: source yield 18–20 pieces. Soak rice overnight, grind with coconut, add yeast and sugar, ferment about 3 hours until risen, salt, fill greased molds halfway and steam 12–15 minutes. Estimated serving basis: two pieces per person.'
        r.tasks=[
          step('rinse','Rinse rice and cover with water',5,'Rinse parboiled rice and cover generously with water for the overnight soak.',ahead=24),
          step('soak','Soak rice overnight',720,'Leave the rice soaking overnight; drain before grinding.',deps=['rinse'],active=0,ahead=24),
          step('batter','Grind rice and coconut; mix in yeast and sugar',25,'Drain rice. Grind rice and coconut finely with enough coconut water for a thick batter, then stir in yeast and sugar.',deps=['soak'],ahead=None),
          step('rise','Let batter rise until bubbly',180,'Allow about 3 hours in a warm spot. Continue when visibly risen and bubbly; use the batter once ready.',deps=['batter'],active=0,ahead=None),
          step('steam','Fill molds, steam and unmold sannas',40,'Fold salt into risen batter. Half-fill greased molds and steam until set; the source gives 12–15 minutes. Let them firm briefly before unmolding.',deps=['rise'],active=25,resource='stovetop',ahead=None,segments=[(0,15),(30,10)])]
    elif 'Without Alcohol' in r.title:
        r.tasks=[
          step('fruit','Chop dried fruit and add orange juice',15,'Chop the dried fruit, mix with orange juice and mixed spice, and cover.',ahead=84),
          step('soak','Soak fruit for 6–8 hours or overnight',480,'Leave covered until the fruit has absorbed the juice.',deps=['fruit'],active=0,ahead=84),
          step('bake','Mix fruit cake batter and bake',210,'Line the tin and preheat to 120°C. Mix butter, sugar, eggs and remaining ingredients; fold in fruit with its juice and nuts. Bake 2½–3 hours, checking for browning after 1½ hours. A skewer should come out clean.',deps=['soak'],active=40,resource='oven',ahead=72,segments=[(0,30),(120,5),(205,5)]),
          step('cool','Cool cake in its tin, then on a rack',140,'Leave in the tin for 20 minutes, then unmold onto a rack. Wrap only when completely cool. Make within 3 days of serving; freeze for longer storage.',deps=['bake'],active=5,ahead=72,segments=[(20,5)])]
    elif 'Doce' in r.title:
        r.tasks=[
          step('rinse','Rinse chana dal and cover with water',5,'Rinse the dal thoroughly and cover with plenty of water.',ahead=48),
          step('soak','Soak chana dal',360,'Soak for 5–6 hours or overnight, then drain.',deps=['rinse'],active=0,ahead=48),
          step('cook','Cook dal until soft; cool and blend with coconut',85,'Pressure-cook dal until soft using your cooker instructions; let pressure release before opening. Drain and reserve the liquid. Cool enough for your blender, then blend dal and coconut separately using minimal reserved liquid.',deps=['soak'],active=30,resource='instant_pot',ahead=48,segments=[(0,5),(45,5),(65,20)]),
          step('stir','Stir the doce until thick, then shape and cut',65,'Stir dal, coconut and sugar continuously as it thickens. Add cardamom and ghee. When it forms a nonsticky dough, spread on a greased surface, mark a pattern, cool briefly and cut.',deps=['cook'],resource='stovetop',ahead=48),
          step('cool','Let doce cool fully',120,'Leave pieces to cool before separating and packing. For this ahead-of-time plan, refrigerate in a covered container once cool.',deps=['stir'],active=0,ahead=48)]
    else: return None
    r.reviewed=True
    r.uncertainties=['Task durations and make-ahead allowances are estimates; use doneness cues.', 'Doce refrigeration for this plan is a conservative planning choice, not a publisher shelf-life claim.'] if 'Doce' in r.title else ['Task durations are estimates; use doneness cues.']
    r.preparation_provenance['christmas_review']='2026-10-29: task-specific instructions, explicit prerequisites, waiting separated, no standalone measuring tasks. '+r.source
    return r
