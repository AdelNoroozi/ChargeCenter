# ChargeCenter

## project development setup

1- compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd ChargeCenter
```

2- create your env
```
python3 -m venv <virtual-environment-name>
source <virtual-environment-name>/bin/activate
cp .env.example .env
```

3- install requirements
```
pip install requirements_dev.txt
```

4- spin off docker compose
```
docker compose -f docker-compose.dev.yml up
```

5- make migrations
```
python manage.py makemigrations
python manage.py migrate
```

6- run project
```
python manage.py runserver
! In development, django project runs seperately from docker services. That's because it makes it easier to develop and does not need building the docker image over and over again. In production everything runs through docker.
```