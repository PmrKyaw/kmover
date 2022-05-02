from app import db 
from sqlalchemy.orm import relationship

class QuoteLimit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey("quote.id"))
    limit_count = db.Column(db.Integer, nullable=False)

    quote = relationship("Quote", back_populates="quote_limit")

    @staticmethod
    def create(quote, limit_count):

        the_limit = QuoteLimit(
            limit_count = limit_count,
            quote = quote,
        )

        db.session.add(the_limit)
        db.session.commit() 

        return the_limit.limit_count

    def __repr__(self):
        return '<QuoteLimit %r>' % self.limit_count

