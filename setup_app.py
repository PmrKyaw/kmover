import os 

def setup():

    run_list = [
        'pip install -r requirements.txt ',
        'flask db init', 
        'flask db migrate',
        'flask db upgrade', 
        'flask add_districts',
    ]

    for i in run_list:
        os.system(i)

    return 

setup()
