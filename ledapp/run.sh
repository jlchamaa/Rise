cd ~/Rise/ledapp/
. venv/bin/activate
export FLASK_APP=ledapp.py
export PYTHONPATH=$PYTHONPATH:$(pwd)
flask run --host=0.0.0.0
