from app import app
import os 
import json 
import requests 
import datetime 

@app.cli.command("test_store_quote")
def test_store_quote(): 
    """Ensure the quote store work correctly."""
    test_quote_one()
    return 

def test_quote_one():
    next_two_day = (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    obj = {"salutation":"Mr.","name":"Kyaw","email":"kyaw.kmover2@gmail.com","district_from":"1","district_to":"3","msg":"","est_move_date": next_two_day,"ph_num":"+12015550127","verify_code":"333333"}
    status = False  

    for i in range(1, 4):
        r = requests.post("http://127.0.0.1:5000/store/quote", json=obj)
        if i == 3: 
            r_dict = json.loads(r.text)
            status = r_dict["status"]
    if status: 
        print("Insertion successful")
    else:
        print("Correctly protect not to store the user with the same email or phone number, and if that user last sent estimated move date is greater than or equal to today.")
