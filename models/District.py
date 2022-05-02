from app import db 
class District(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return '<District %r>' % self.name