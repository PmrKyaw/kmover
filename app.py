import os 
import datetime

from flask import Flask, request, render_template, redirect, session, make_response, jsonify, abort, url_for
from sqlalchemy import desc, asc
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from sqlalchemy import or_

from flask_wtf.csrf import CSRFProtect

from werkzeug.datastructures import MultiDict


app = Flask(__name__)


app.config.from_object("config.DevelopmentConfig")
Session(app)


csrf = CSRFProtect(app)
csrf.init_app(app)


db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models.District import District
from models.Quote import Quote
from models.QuoteLimit import QuoteLimit

from form import PsiForm, PhoneForm

from helpers import hasSend, overLimit
from db_setup import add_district

db.init_app(app)


if __name__ == "__main__":
    app.run()


@app.route("/")
def index():
    # get all the districts from database 
    districts = District.query.all()  
    return render_template("index.html", districts=districts)

@app.route('/faq')
def q_and_a():
    return render_template("q_and_a.html")

@app.route("/about-us")
def about_us():
    return render_template("about_us.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/contact-us")
def contact_us():
    return render_template("contact_us.html")

@app.route("/quoted/success")
def quoted():
    # ensure the user already successfully sent the quote 
    if session.get("quoted") == True:
        session.pop("quoted")
        return render_template("quoted.html")
        
    return redirect("/")

    
@app.route("/quote/psri", methods = ["GET", "POST"])
def psri():

    # get all the districts 
    districts = District.query.all() 

    # get the district_from and district_to from request 
    req_district_from = request.args.get("district_from")
    req_district_to = request.args.get("district_to")

    groups_list = [(district.id, district.name) for district in districts]

    # make form 
    form = PsiForm(request.form)

    # dynamic choices 
    form.district_from.choices = groups_list
    form.district_to.choices = groups_list

    if request.method == "GET":
        # reset the verify session 
        if session.get("verify") == True:
            session["verify"] = False 
    
    if request.method == "POST":
        
        if form.validate():

            # if the user already verify redirect back 
            if session.get("verify") == True:
                return redirect(request.url)

            session["verify"] = True 
            return render_template("info_psr.html", form=form)

    return render_template("personal_info.html", form=form, districts=districts, req_district_from=req_district_from, req_district_to=req_district_to)

@app.route("/info/verify", methods = ["POST"])
def info_verify():

    # ensure the request is application/json 
    try:
        json_data = request.get_json(force=True)
    except:
        abort(400)

    # init variables
    valid = False 
    ph_num = ''
    verify_code = ''

    # ensure the data are in json request 
    if "ph_num" in json_data:
        ph_num = json_data["ph_num"]
    if "verify_code" in json_data:
        verify_code = json_data["verify_code"]

    # create multidict 
    l = MultiDict([("ph_num", ph_num), ("verify_code", verify_code)])
    
    form = PhoneForm(l)

    # check the code is valid or not 
    if form.validate() and verify_code == '333333':
        session["can_store"] = True 
        valid = True 

    return make_response(jsonify({
        "valid": valid
    }), 200)

@app.route('/store/quote', methods = ["POST"])
# @csrf.exempt # user for testing 
def quote():

    # only the user who already verify the user information and 
    # phone number can store quote 
    if session.get("can_store") != True:
        abort(400)

    # ensure the request is application/json 
    try:
        json_data = request.get_json(force=True)
    except:
        abort(400)

    # init variables 
    status = True 

    valid = True 

    msg = ''

    usp = []

    tp = []

    name = ''
    
    # add the necessary to tp or telphone list
    # add the necessary to usp or user information 
    for j in json_data:

        if j == "ph_num" or j == "verify_code":
            tp.append((j, json_data[j].strip()))
        else:
            usp.append((j, json_data[j].strip()))

    # same logic 
    districts = District.query.all() 

    groups_list = [(district.id, district.name) for district in districts]

    # create multidict
    uinfo_form = PsiForm(MultiDict(usp))
    phvf_form = PhoneForm(MultiDict(tp))
    # for testing 
    # uinfo_form = PsiForm(MultiDict(usp), meta={'csrf': False})
    # phvf_form = PhoneForm(MultiDict(tp), meta={'csrf': False})

    # dynamic choices 
    uinfo_form.district_from.choices = groups_list
    uinfo_form.district_to.choices = groups_list

    # ensure both user information, phone number are correct 
    if not uinfo_form.validate() or not phvf_form.validate():
        valid = False 
        status = False
    if valid:
        sended = hasSend(json_data["email"], json_data["ph_num"])

        # create new record for the new user 
        if sended is None:
            quote = Quote.create(json_data)
            limit = QuoteLimit.create(quote, 1)
        else:
            # check the quote limit 
            over = overLimit(sended)

            if over == "update":
                Quote.update(sended, json_data)
            elif over == "recreate":
                Quote.update(sended, json_data, recreate=True)
            else:
                status = False 
                msg = """
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Soory!</strong> You can't send quote right now.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                """

        if status:
            session["quoted"] = True 
            name = json_data["name"]

    return make_response(jsonify({
        'msg': msg,
        'name': name,
        'valid': valid,
        'status': status,
    }), 200)