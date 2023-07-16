# Serverless google auth login

AWS serverless lambda function using Flask to handle google authentication.

**Endpoints**:

- **Login ("/login")**: Redirects to google login authentication page.
- **Login Callback ("/login/callback")**: Handle the callback right after google login authentication, gets user info then return auth token as queryparam.

## Install requirements

```sh
python -m pip install -r -requirements.txt
```

## Install node requirements

```sh
npm install
```

## Install sls plugins

```sh
serverless plugin install -n serverless-wsgi
serverless plugin install -n serverless-python-requirements
```

## Run app locally

   1. Create a .env file with:

      ```env
      STAGE=local
      OAUTH_CLIENT_ID=[YOUROAUTHCLIENTID]
      OAUTH_CLIENT_SECRET=[YOUROAUTHCLIENTSECRET]
      ```

   2. Run app

      ```sh
      python app.py
      ```

It should runs at https://127.0.0.1:5000

## Run tests

```sh
pytest test/
```

## Deploy app

```sh
sls deploy --aws-profile [YOURAWSPROFILE]
```

## Deploy app pushing to master branch

1. Create a github repository with master as main branch.
2. CI/CD should execute when you push to master

***Important: Set the next env vars on AWS lambda function configuration after deploy:***

```env
LAMBDA_URL=[YOURLAMBDAHOSTURL]
OAUTH_CLIENT_ID=[YOUROAUTHCLIENTID]
OAUTH_CLIENT_SECRET=[YOUROAUTHCLIENTSECRET]
```

***Annotation: Remove CORS related code before deploy on production.***
