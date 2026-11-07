"""Source-reviewed corrections found by the free-calendar scenarios."""
from simmer.domain import AttentionSegment,PrepTask
VEGETARIAN={'Butter Paneer {Paneer Makhani}','Instant Pot Chana Masala (Punjabi Chole)','Vegetable Pulao Recipe | Veg Pulav','Instant Pot Rice Pudding','Instant Pot Dal Makhani','Instant Pot Carrot Halwa Recipe'}
def refine(recipe):
 r=recipe.model_copy(deep=True)
 if r.title in VEGETARIAN:r.vegetarian=True
 def attention(task,segments):
  task.attention_segments=[AttentionSegment(offset_minutes=o,minutes=m) for o,m in segments]
  task.active_minutes=sum(m for _,m in segments);task.presence_minutes=task.active_minutes
 if r.source.rstrip('/')=='https://ministryofcurry.com/rice-pudding-instant-pot':
  for t in r.tasks:
   t.preparation_policy='advance';t.max_ahead_hours=24;t.max_dependency_gap_minutes=15 if t.dependencies else None
  attention(r.tasks[1],[(0,5)])
  attention(r.tasks[3],[(0,5),(30,5)])
  r.tasks[3].title='Cool in shallow containers and refrigerate; serve chilled'
  r.tasks[3].guidance='Divide into shallow containers and refrigerate promptly. Keep chilled until serving. A one-day make-ahead allowance is a planning estimate; the source supports making ahead and serving chilled.'
  r.preparation_provenance['realistic_review']='Source supports make-ahead and chilled serving; 24-hour allowance and attention segments are planning estimates.'
 if r.source.rstrip('/')=='https://ministryofcurry.com/instant-pot-chana-masala-recipe':
  for t in r.tasks:
   if t.id=='reviewed-step-3':attention(t,[(0,5),(60,5)])
  r.preparation_provenance['realistic_review']='Pressure cooking and natural release retain the 65-minute elapsed allowance; start/end attendance estimated at 10 minutes. Source method retained.'
 if r.source.rstrip('/')=='https://ministryofcurry.com/paneer-butter-masala':
  attention(r.tasks[1],[(0,10),(20,5)])
  r.preparation_provenance['realistic_review']='Retains 25-minute sauce step; estimated attention covers saute/setup and return. Pressure time remains unchanged.'
 if r.source.rstrip('/')=='https://www.wellplated.com/old-fashioned-sweet-potato-pie':
  for t in r.tasks:
   t.preparation_policy='advance';t.max_ahead_hours=48;t.max_dependency_gap_minutes=15 if t.dependencies else None
  attention(r.tasks[0],[(0,15)])
  attention(r.tasks[4],[(0,5),(15,5),(60,5)])
  old=next(t for t in r.tasks if t.id=='reviewed-step-6')
  old.title='Cool pie on a rack, then cover and refrigerate'
  old.minutes=115;attention(old,[(110,5)])
  old.guidance='Cool on a rack and refrigerate within two hours of baking. Keep refrigerated until serving; the source supports preparing one or two days ahead.'
  r.tasks=[t for t in r.tasks if t.id!='whipped-cream']
  r.tasks.append(PrepTask(id='whipped-cream',title='Whip optional cream and refrigerate separately',minutes=15,active_minutes=15,presence_minutes=15,dependencies=[old.id],preparation_policy='advance',max_ahead_hours=24,evidence=r.source,guidance='Whip cream with the optional topping ingredients; refrigerate until serving.',timing_basis='estimate'))
  r.preparation_provenance['realistic_review']='Source explicitly supports 1–2 days ahead and refrigerated storage. Cooling/cream separated; estimated attendance preserves baking duration.'
 return r
