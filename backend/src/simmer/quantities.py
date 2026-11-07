"""Lossless quantity annotations; uncertain text is never replaced with a guess."""
import re
from .domain import QuantityDetail

def describe_amount(row):
    if row.amount_detail is not None:
        return row.amount_detail
    text=row.name
    optional=bool(re.search(r'\boptional\b',text,re.I))
    kind='exact' if row.quantity is not None else 'unknown'
    if kind=='unknown' and re.search(r'\b(to taste|as needed|as required)\b',text,re.I):
        kind='to_taste'
    return QuantityDetail(kind=kind,optional=optional,source_text=text)

def scale_amount(row, ratio):
    detail=describe_amount(row).model_copy(deep=True)
    updates={'amount_detail':detail}
    if ratio is None:
        updates['quantity']=None
        updates['amount_detail']=QuantityDetail(kind='unknown',source_text=detail.source_text,optional=detail.optional)
    elif detail.kind=='range':
        updates['amount_detail']=QuantityDetail.model_validate(detail.model_dump() | {'minimum':detail.minimum*ratio,'maximum':detail.maximum*ratio})
        updates['quantity']=None
    elif row.quantity is not None:
        updates['quantity']=row.quantity*ratio
    return row.model_copy(update=updates)
