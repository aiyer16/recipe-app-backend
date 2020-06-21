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

## Useful commands

### Start all container services

```sh
# Must be root directory
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