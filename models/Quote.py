from datetime import datetime
from app import db
from sqlalchemy.orm import relationship
from werkzeug.datastructures import MultiDict


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


    def get_multi(self):
        l = [
            ("salutation", self.salutation), ("name", self.name), ("email", self.email),
            ("ph_num", self.phone),
            ("district_from", self.move_from), ("district_to", self.move_to),
            ("est_move_date", self.estimated_move_date.strftime("%Y-%m-%d")), ("msg", self.message)
        ]
        return MultiDict(l)

    def to_dict(self):
        return {
            "salutation": self.salutation,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "move_from": self.t_move_from[0].name,
            "move_to": self.t_move_to[0].name,
            "estimated_move_date": self.estimated_move_date.strftime("%Y-%m-%d"),
            "status": self.status,
            "msg": self.message
        }
        

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

        return quote

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

    @staticmethod
    def action(info, req_form, only_status=False):

        if only_status:
            user = info 
            user.status = req_form["take_action"]
            
            db.session.add(user)
            db.session.commit()
            return req_form["take_action"]

        else:
            user = info 
            user.salutation=req_form["salutation"]
            user.name=req_form["name"]
            user.email=req_form["email"]
            user.phone=req_form["ph_num"]
            user.move_from=req_form["district_from"]
            user.move_to=req_form["district_to"]
            user.message=req_form["msg"]
            user.estimated_move_date=datetime.strptime(req_form["est_move_date"], "%Y-%m-%d")
            user.status=req_form["take_action"]

            db.session.commit() 
            return req_form["take_action"]


    def __repr__(self):
        return '<Quote %r>' % self.name