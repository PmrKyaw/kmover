import os 

def setup():

    run_list = [
        'pip install -r requirements.txt ',
        'flask db init', 
        'flask db migrate',
        'flask db upgrade', 
        'flask add_districts',
        'export FLASK_ENV=development',
        'export FLASK_DEBUG=True',
        'flask run'
    ]

    for i in run_list:
        os.system(i)

    return 
