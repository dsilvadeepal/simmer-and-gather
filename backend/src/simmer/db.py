from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import Base, Document

class Conflict(ValueError): pass
class Missing(ValueError): pass

class Store:
    def __init__(self, url):
        if not url.startswith('postgresql'): raise ValueError('PostgreSQL required')
        self.engine=create_engine(url, pool_pre_ping=True)
    def create_schema(self): Base.metadata.create_all(self.engine)
    def get(self, owner, kind, id):
        with Session(self.engine) as s:
            row=s.get(Document,(owner,kind,id))
            if row is None: raise Missing('Record not found')
            return row.body, row.revision
    def list(self, owner, kind):
        with Session(self.engine) as s:
            return [r.body for r in s.scalars(select(Document).where(Document.owner==owner,Document.kind==kind))]
    def put(self, owner, kind, id, body, expected=None):
        try:
            with Session(self.engine) as s, s.begin():
                if expected is None:
                    s.add(Document(owner=owner,kind=kind,id=id,revision=1,body=body))
                    return 1
                revision=expected+1
                result=s.execute(update(Document).where(Document.owner==owner,Document.kind==kind,Document.id==id,Document.revision==expected).values(body=body,revision=revision))
                if result.rowcount!=1: raise Conflict('This record changed; reload before saving')
                return revision
        except IntegrityError as e: raise Conflict('Record already exists') from e
