from datetime import date, datetime
from sqlalchemy import or_
from app import db, Quote

def hasSend(email, phone):
    c = Quote.query.filter(or_(Quote.email==email, Quote.phone==phone)).first()
    return c

def overLimit(q):
    if q.quote_limit.limit_count < 3:
        return "update"
    else:
        if q.quote_limit.limit_count == 3 and date.today() > q.estimated_move_date:
            return "recreate"
        
        return "over"