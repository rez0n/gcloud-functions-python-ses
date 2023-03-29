# Google Cloud Functions: Send Email using AWS SES
This function will send templated (by Jinja) email message with image attachment using AWS SES to the specified email address. 
May be useful for landing (marketing) static website which contains "Contact Us" form.

## Deploy
```
gcloud functions deploy <function-name> \
--runtime=python311 \
--region=europe-central2 \
--source=. \
--entry-point=hello_http \
--trigger-http \
--allow-unauthenticated
```

## Configuration
Edit Cloud Function using Google Cloud Console to set **Runtime environment variables** 
(look required variables in `.env.example`)

## Use
```
curl -X POST <FUNCTION_URL> \
   -H "Content-Type: application/json" \
   -d '{"your_name": "Denis"}'
```

## Epilog
- As endpoint can be called from any source it worth to add captcha integration to avoid bots spam you for your money, 
example of [recaptcha implementation](https://github.com/rez0n/digitalocean-functions-python-recaptcha).

