from app import app
import datetime
import phonenumbers
from flask_wtf import FlaskForm
from wtforms import Form, SelectField, DateField, BooleanField, StringField, PasswordField, validators, ValidationError, TextAreaField, IntegerField


class PsiForm(FlaskForm):
        
    salutation = SelectField('Salutation', choices = [('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Dr.', 'Dr.')], validators = [validators.InputRequired(message="Enter a Given Salutation or Gender")])
    name = StringField('Name', validators = [validators.Length(min=4, max=20, message="Name need to be at least 4 characters, and up to 20 max characters"), validators.InputRequired("Enter your Name")])
    email = StringField('Email', validators = [validators.InputRequired(message="Enter Email"), validators.Email(message="Email is invalid!")])
    district_from = SelectField('Moving From', coerce=int, validators=[validators.InputRequired(message="Can't be blank!")])
    district_to = SelectField('Moving To', coerce=int, validators=[validators.InputRequired(message="Can't be blank!")])
    est_move_date = DateField('Estimated Move Date', validators=[validators.InputRequired(message="Estimated move date can't be empty!"), validators.DataRequired(message="Invalid date")])
    msg =  TextAreaField('Message', [validators.optional(), validators.length(max=200)])


    def validate_est_move_date(self, est_move_date):
        es_date = est_move_date.data

        if es_date != None:
            if es_date <= datetime.date.today():
                raise ValidationError('Date can\'t be past!')
        

class PhoneForm(FlaskForm):
    ph_num = StringField('Phone', validators= [validators.InputRequired()])
    verify_code = StringField('Verify Code', validators= [validators.Length(min=6, max=6), validators.InputRequired()])

    def validate_ph_num(self, ph_num):
        try:
            p = phonenumbers.parse(ph_num.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
