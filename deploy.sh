
gcloud functions deploy ses_email \
--runtime python39 \
--trigger-http \
--region=europe-west3 \
--entry-point=main \
--allow-unauthenticated \
--project=quaded