from datetime import datetime
from app import db
from sqlalchemy.orm import relationship


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    salutation = db.Column(db.VARCHAR(10), nullable=False)
    name = db.Column(db.VARCHAR(40), nullable=False)
    email = db.Column(db.VARCHAR(100), nullable=False)
    phone = db.Column(db.VARCHAR(15), nullable=False)
    move_from = db.Column(db.Integer, db.ForeignKey("district.id"))
    move_to = db.Column(db.Integer, db.ForeignKey("district.id"))
    message = db.Column(db.Text, nullable=True)
    estimated_move_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.VARCHAR(40), default="sended", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    quote_limit = relationship(
        "QuoteLimit", 
        cascade='all, delete-orphan',
        back_populates="quote", 
        uselist=False,
        single_parent=True,
    )

    t_move_from = relationship("District", primaryjoin="Quote.move_from==District.id", uselist=True)
    t_move_to = relationship("District", primaryjoin="Quote.move_to==District.id", uselist=True)


    @staticmethod
    def create(json_data, with_status=False):
        quote = Quote(
            salutation=json_data["salutation"],
            name=json_data["name"],
            email=json_data["email"],
            phone=json_data["ph_num"],
            move_from=json_data["district_from"],
            move_to=json_data["district_to"],
            message=json_data["msg"],
            status= json_data["status"] if with_status else "sended",
            estimated_move_date=datetime.strptime(json_data["est_move_date"], "%Y-%m-%d")
        )

        db.session.add(quote)

        db.session.commit() 

    @staticmethod
    def update(info, json_data, recreate=False):

        user = info 
        user.salutation=json_data["salutation"]
        user.name=json_data["name"]
        user.email=json_data["email"]
        user.phone=json_data["ph_num"]
        user.move_from=json_data["district_from"]
        user.move_to=json_data["district_to"]
        user.message=json_data["msg"]
        user.estimated_move_date=datetime.strptime(json_data["est_move_date"], "%Y-%m-%d")

        if not recreate:
            user.quote_limit.limit_count += 1 
        else:
            user.quote_limit.limit_count = 1 

        db.session.commit() 

    def __repr__(self):
        return '<Quote %r>' % self.name