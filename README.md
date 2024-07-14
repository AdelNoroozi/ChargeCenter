<h1>Charge Center</h1>

# Introduction
<img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/banner.jpg" >
A DRF web application for selling phone number charges with the ability of running under high loads without transaction conflicts.

API documentations can be found in the base url of the project.


# Tools
<div style ="display: flex;">
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/python-icon.png" >
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/django-icon.png" >
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/rest-api-icon.png" >
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/postgresql-icon.png" >
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/jwt-icon.png" >
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/flask-icon.png" >
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/gunicorn-icon.png" >
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/locust-icon.png" >
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/docker-icon.png" >
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/cookiecutter-icon.png" >
  <img src="https://github.com/AdelNoroozi/ChargeCenter/blob/master/resources/swagger-icon.png" >
</div>
- I have used this cookiecutter for my project structure:

https://github.com/AdelNoroozi/Personal-Cookiecutter

- In this structure the main configuration and setting files are inside the config directory and the django apps are inside the chargecenter (project_slug) directory. Requirements and Docker related files are seperated for development and production processes. (for example The main django app is not included in docker development services to avoid rebuilding project after every modification in code.)

- This project uses Django & Django REST framework for handling APIs.

- All the queries are written through selector functions which can be found inside the selectors directory in each app. The main business logic of the project is defined as services which are the python functions inside services directories. Serializers are also used for validating data or defining data structures. No Generic API View was used in this project because of the SOA architecture and all the API classes (in apis.py file inside the apps) inherit from APIViews. 

- PostgreSQL is used as the database for this project. The PostgreSQL's full-text-search tools are used in this project for better search results. To do so, a PostgreSQL extension called pg_trgm is needed. The process of its installation is handled through a migration file inside the core app (chargecenter/core/migrations/0001_install_pg_trgm.py). The package will be installed when running the django migrate command and there is no need for manual installation of this extension inside the database.

- The rest_framework_simplejwt package is used for authentication. The API classes inherit from two custom mixins for authentication & authorization called ApiAuthMixin and BasePermissionsMixin (chargecenter/api/mixins.py). The ApiAuthMixin class is used to access the user requesting when it is needed through business logic. The BasePermissionsMixin defines the logic of API permissions by the HTTP method. There is a dictionary which by default states that HTTP requests with GET methods can be sent by any user, but staff privileges is needed for other methods. This dictionary can be overwritten in any API class if needed.

- The Flask Python microframework is used for mocking an external charging service. 

- Gunicorn is used as a server both for running the main Django app (in production layer) and for running the Flask mocking service.

- Locust is used for putting high loads with high RPS (request per second) to simulate complicated scenarios in production level.

- This project is containerized using Docker compose.

- The drf_spectacular package is used for documentation of this project. It generates a great UI for working with APIs and also provides the whole authentication functionalities. This UI is accessible inside the base url of the project after running it. Defining these docmentations is done inside the files found in the documentations directory of each app. Request body structure for POST requests, possible respones, parameters & query parameters are described inside the swagger UI for most of the APIs.

# Setup
For running the project, follow the steps bellow.

1-Create a virtual environment:
```bash
virtualenv Venv
```
2-Activate virtual environment:
```bash
source Venv/bin/activate
```
3-Install the requirements:
```bash
pip install -r requirements_dev.txt
```
4-run the development docker services. The main django app is not included in docker development services to avoid rebuilding project after every modification in code.
```bash
docker compose -f docker-compose.dev.yml up
```

for running the whole project at once and bypassing steps 6 & 7, run this command:
```bash
docker compose -f docker-compose.yml up
```
5-Add your .env file in the root directory. There are some default values to avoid any improperly configured exceptions, but for better functionality it's for best to include the environment variables using a .env file. The only part of the app that won't work without these configurations are the email sending services which the required settings could be find in "config/settings/email_sending.py". The app will still work without those settings but no emails would be sent. 

Database settings can also be configured in the .env file, otherwise the app will use the database inside the docker services.

IMPORTANT: The database for this project MUST BE a Postgresql database, because the food search engine uses some functionalities which are only provided by Postgresql databases. For more information go to the part about "searching foods" in the description part.

6- Migrate.
```bash
python manage.py migrate
```

7- Run the project:
```bash
python manage.py runserver
```
8- Create a superuser for using the APIs that need staff privileges or accessing the admin panel (optional):
```bash
python manage.py createsuperuser
```
