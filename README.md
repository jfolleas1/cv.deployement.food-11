# Deployement of your image recognition model

## Set up the virtual env
`virtualenv venv`

`source venv/bin/activate`

`pip install -r predictor_requirements.txt`

## Run flask localy (NOT FOR PRODUCTION)

python predictor.py

## Run flask with gunicorn local (For pre-production testing)

`gunicorn -b 0.0.0.0:8080 predictor:app`

