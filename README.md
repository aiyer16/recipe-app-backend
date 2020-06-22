# recipe-app-api
REST API for a simple Recipe application created using Django REST framework and Postgres database. Clone this repository to use as template to fulfill all your REST API needs. 

## Getting Started

### Configure environment variables
Create a new .env file in the directory with the following variables defined. Feel free to customize username/password as per your requirements.

```
DB_HOST=recipe-app-api-db
DB_NAME=app
DB_USER=postgres
DB_PASS=supersecretpassword
PGADMIN_DEFAULT_EMAIL=sysadmin@sysadmin.com
PGADMIN_DEFAULT_PASSWORD=supersecretpassword
```

### Start all container services
Running this command for the first time will automatically build the required images.

```sh
# Must be run from root directory
docker-compose up
```

- REST API is available at http://localhost:8000 (admin screen available at http://localhost:8000/admin)
- PGAdmin 4 is available at http://localhost:8080
- Database host is available at recipe-app-api-db

### Create a new super user
To access the admin screen, you must first create a superuser using the following command. Follow the instructions to create a username/password, which can then be used to login in the admin screen.

```sh
docker-compose run --rm recipe-app-api-server sh -c "python manage.py createsuperuser"
```

### Creating site users
There is currently no end-point for managing users for the site, so you will need to do this from the Django admin screen. Login to the Django admin screen using your superuser credentials and add a new user from within the Authentication and Authorization panel.

![Create site user](/images/CreateSiteUser.png)

### Run all tests
At this point it is a good idea to run all tests to confirm that the site is working as expected before you can go ahead with browsing all available end-points. 

```sh
docker-compose run --rm recipe-api-app-server sh -c "python manage.py test && flake8"
```

## API Endpoints
Navigating to http://localhost:8000/api/index will provide you a swagger style documentation for all the endpoints for this API. 

![Swagger API Docs](/images/SwaggerIndexPage.png)

### Authentication
All the endpoints for the recipe app are gated behind token based authentication. You can use the following endpoints to login/logout by generating/destroying token(s). 

- /auth/token/login: Generate a token by supplying a site username/password
- /auth/token/logout: Destroy generated token that is supplied via request header.

The token generated here must be supplied to all other endpoints in this app or the Unauthorized Request will be generated. If you're using the swagger style browsable API, you can supply this easily using the Authorize button and entering the token as follows. Once logged in, all endpoints will be available. 

![Swagger token authorization](/images/SwaggerTokenAuthorize.png)

### Recipe
#### Ingredients
http://localhost:8000/api/recipe/ingredients   
http://localhost:8000/api/recipe/ingredients/{id}
- Allowed Methods: GET, POST
- Returns ingredients tied to logged in user or all ingredients if user is a superuser. 

#### Tags
http://localhost:8000/api/recipe/tags   
http://localhost:8000/api/recipe/tags/{id}
- Allowed Methods: GET, POST
- Returns tags tied to logged in user or all tags if user is a superuser. 

#### Recipes
http://localhost:8000/api/recipe/recipes   
http://localhost:8000/api/recipe/recipes/{id}
- Allowed Methods: GET, POST
- Returns recipes tied to logged in user or all recipes if user is a superuser. 

## Useful commands

### Start all container services

```sh
# Must be run from root directory
docker-compose up
```

### Run all tests

```sh
docker-compose run --rm recipe-api-app-server sh -c "python manage.py test && flake8"
```

### Make migrations (run once for each new model added)

```sh
# Last parameter is the app name, example "recipe"
docker-compose run --rm recipe-app-api-server sh -c "python manage.py makemigrations recipe"
```