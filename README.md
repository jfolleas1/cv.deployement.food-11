# Deployement of your image recognition model

## Set up the virtual env
`virtualenv venv`

`source venv/bin/activate`

`pip install -r predictor_requirements.txt`

## Run flask localy (NOT FOR PRODUCTION)

python predictor.py

## Run flask with gunicorn local (For pre-production testing)

`gunicorn -b 0.0.0.0:8080 predictor:app`

## Deployement on GCP

Doc : https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python

`export PROJECT_ID=train-food-11-classification`

`export IMAGE_URI=eu.gcr.io/$PROJECT_ID/food_predictor_app`

`gcloud builds submit --tag $IMAGE_URI` /!\ it uses the gitignore

`gcloud run deploy --image $IMAGE_URI --platform managed`

gcloud run deploy --image $IMAGE_URI --platform managed --memory 2.0G

go in cloud run GCP service to see your running app


annex: 


gcloud config get-value project

TODO :

Allow unauthenticated invocations to [foodpredictorapp] (y/N)? -> How to set to No