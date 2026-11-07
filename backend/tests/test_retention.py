from datetime import datetime, timezone, timedelta
from io import BytesIO
from PIL import Image
import pytest
from simmer.adapters.storage import UploadStore
from simmer.db import Missing

def test_upload_scope_signature_and_independent_expiration(store,owner):
    now=datetime.now(timezone.utc); service=UploadStore(store)
    with pytest.raises(ValueError): service.upload(owner,b'fake','image/png',now)
    out=BytesIO(); Image.new('RGB',(5,5)).save(out,format='PNG')
    id=service.upload(owner,out.getvalue(),'image/png',now)
    with pytest.raises(Missing): service.read('another',id,now)
    assert service.read(owner,id,now)
    service.cleanup(now+timedelta(days=8))
    with pytest.raises(Missing): service.read(owner,id,now+timedelta(days=8))
