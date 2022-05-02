from app import app
import os 
import json 
import requests 

@app.cli.command("setup")
def test_multiple():

    run_list = [
        'python -m env ./env',
        'source ./env/bin/activate',
        'pip install -r requirements.txt ',
        'flask db init', 
        'flask db migrate',
        'flask db upgrade', 
        'flask add_districts',
        'flask run'
    ]

    for i in run_list:
        os.system(i)

    print('Done.')
    return 


@app.cli.command("test_store_quote")
def test_store_quote(): 
    """Ensure the quote store work correctly."""
    obj = {"salutation":"Mr.","name":"Kyaw","email":"kyaw.kmover2@gmail.com","district_from":"30","district_to":"32","msg":"","est_move_date":"2022-05-02","ph_num":"+12015550127","verify_code":"333333"}

    status = False  

    for i in range(1, 4):
        r = requests.post("http://127.0.0.1:5000//store/quote", json=obj)
        if i == 3: 
            r_dict = json.loads(r.text)
            status = r_dict["status"]

    if status: 
        print("Insertion successful")
    else:
        print("Correctly protect not to store the user with the same email and phone number, move date nothing more than three time.")
    print(status)
    return 
