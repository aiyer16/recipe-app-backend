# recipe-app-api
REST API for the Recipe App created using Django REST framework

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