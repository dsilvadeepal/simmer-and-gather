"""Private PostgreSQL upload storage for low-volume prototype; no public URLs.

Seven-day hard expiry starts at upload (stricter than extraction +7 days).
Production release needs the independent pg_cron cleanup installed and verified.
"""
import base64, hashlib, io
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from PIL import Image
from sqlalchemy import delete
from ..models import Document
from ..db import Missing

class UploadStore:
    def __init__(self,store): self.store=store
    def upload(self,owner,content,mime,now):
        if not 0<len(content)<=10*1024*1024: raise ValueError('Image limit is 10 MB')
        formats={'image/png':'PNG','image/jpeg':'JPEG','image/webp':'WEBP'}
        if mime not in formats: raise ValueError('Use JPEG, PNG or WebP')
        try:
            im=Image.open(io.BytesIO(content))
            if im.format!=formats[mime] or im.width*im.height>25_000_000: raise ValueError()
            im.verify()
        except Exception as e: raise ValueError('Invalid or oversized image') from e
        digest=hashlib.sha256(content).hexdigest()
        for old in self.store.list(owner,'upload'):
            if old['sha256']==digest and datetime.fromisoformat(old['expires_at'])>now: return old['id']
        id=str(uuid4()); body={'id':id,'mime':mime,'sha256':digest,'content':base64.b64encode(content).decode(),'expires_at':(now+timedelta(days=6,hours=23)).isoformat()}
        self.store.put(owner,'upload',id,body); return id
    def read(self,owner,id,now):
        body,_=self.store.get(owner,'upload',id)
        if datetime.fromisoformat(body['expires_at'])<=now: raise Missing('Upload expired')
        return body
    def delete(self,owner,id):
        with self.store.engine.begin() as c: c.execute(delete(Document).where(Document.owner==owner,Document.kind=='upload',Document.id==id))
    def cleanup(self,now):
        # Independent maintenance entry point; no user session or calendar activity required.
        from sqlalchemy import cast, DateTime
        with self.store.engine.begin() as c:
            c.execute(delete(Document).where(Document.kind=='upload',cast(Document.body['expires_at'].astext,DateTime(timezone=True))<=now))
