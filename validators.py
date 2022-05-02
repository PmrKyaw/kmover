from app import db, User
from sqlalchemy import or_
from wtforms import ValidationError
from werkzeug.security import check_password_hash

def unique_name(form, field):
    user = User.query.filter_by(name=field.data).first() 
    if user is not None:
        raise ValidationError("Username Taken")

def has_register(form, field):
    if form.password.validate(form): 
        p_user = User.query.filter(or_(User.name==form.cc_info.data, User.email==form.cc_info.data)).first()
        if p_user is None:
            raise ValidationError("There is no user")
        if not check_password_hash(p_user.password, form.password.data):
            raise ValidationError("Invalid crenedital")


            

    # print(form.cc_info.data, form.password.data)

def UniqueEmail(form, field):
    user = User.query.filter_by(email=field.data).first() 
    if user:
        raise ValidationError("Email Taken")