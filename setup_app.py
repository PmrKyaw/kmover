import os 

def setup():

    run_list = [
        'python -m venv ./env',
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

    return 
