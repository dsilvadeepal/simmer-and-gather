"""Refresh shared contracts without constructing an app or opening integrations."""
import json
from pathlib import Path
from simmer.routes import Workspace
root=Path(__file__).resolve().parents[1]
target=root/'frontend/openapi.json'
document=json.loads(target.read_text())
schema=Workspace.model_json_schema(ref_template='#/components/schemas/{model}')
document['components']['schemas'].update(schema.pop('$defs',{}))
document['components']['schemas']['Workspace']=schema
target.write_text(json.dumps(document,indent=2)+'\n')
print('Updated shared schemas. Generate TypeScript with openapi-typescript --default-non-nullable false.')
