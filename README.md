# Django-DRF-CompanyApp
![GitHub repo size](https://img.shields.io/github/repo-size/sDebski/Django-DRF-CompanyApp)
![GitHub last commit](https://img.shields.io/github/last-commit/sDebski/Django-DRF-CompanyApp?color=yellow)
![GitHub top language](https://img.shields.io/github/languages/top/sDebski/Django-DRF-CompanyApp?color=purple)

## ✉️ Technologies used:

- Django
- Celery
- RabbitMQ
- PostgreSQL
- Docker
- Docker Compose

## ✉️ About

Project showing the usage of microservices with event-driven communication.
The idea is based of dividing the functionality of the app to microservices.

## ✉️ Services

- Users - service to manage users, create, update, delete them
- Emails - service to manage emails send to user on changing user model

## ✉️ Setup

- You can download the repo using this code via terminal
```bash
git clone https://github.com/sDebski/Microservices.git
```
- Create .env file based on template.env in app directory
```bash
POSTGRES_DB=dbname
DB_HOST_DEFAULT=psql_db
DB_PORT_DEFAULT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin

MQ_USERNAME=guest
MQ_PASSWORD=guest
MQ_HOST=rabbit_mq
MQ_PORT=5672

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST_USER=system@mail.com
```
## ✉️ Launch

Being in the app folder use command: `docker compose up --build -d`

## ✉️ Inspect

- Open the app in you browser at:
[admin_panel](http://localhost:80/admin/)

- Login to admin panel, create and update users
```bash
login: admin
password: admin
```

- Go into celery container named: `microservices-email-celery-1`
and see that email is being send via console during updating or creating user in users app:

```
2024-03-13 13:29:06 Subject: Welcome!
2024-03-13 13:29:06 From: system@mail.com
2024-03-13 13:29:06 To: test_user@email.com
2024-03-13 13:29:06 Date: Wed, 13 Mar 2024 12:29:06 -0000
2024-03-13 13:29:06 Message-ID: <171033294625.9.8126894065475988290@483b923b9ebd>
2024-03-13 13:29:06
2024-03-13 13:29:06 Hello test_user, here is a message for you
```

