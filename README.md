# Django-DRF-CompanyApp
![GitHub repo size](https://img.shields.io/github/repo-size/sDebski/Django-DRF-CompanyApp)
![GitHub last commit](https://img.shields.io/github/last-commit/sDebski/Django-DRF-CompanyApp?color=yellow)
![GitHub top language](https://img.shields.io/github/languages/top/sDebski/Django-DRF-CompanyApp?color=purple)

## ✉️ Technologies used:

- Django=4.2.15,
- Celery, Celery Beat,
- Redis,
- PostgreSQL,
- Docker,
- Docker Compose,
- Nginx,
- Swagger,
- Poetry,

## ✉️ About

This project demonstrates an app based on DRF, showcasing various Django functionalities.
The database structure used in the project simulates a company.

## ✉️ Topics used in apps:

### Company App
- Custom commands management to populate database based on fixtures
- Integrated swagger to document api structure
  - API Key authentication
  - Knox Token authentication
- Customized admin panel
- Customized exception handler

### Core
- Middleware to log app usage
- Password reset option
- Password validators
- Password history
- App healthcheck endpoints

### Company
- Model fixtures
- Commands on updating statuses
- Signals
- Filtersets
- HistoryLog creator for Task objects changes
- Custom permissions
- Celery tasks
- Celery + Redis RPC
- Caching

### Tests
- Migration tests
- Unit tests
- Integration tests
  

## ✉️ Setup

- You can download the repo using this code via terminal
```bash
git clone https://github.com/sDebski/Django-DRF-CompanyApp.git
```
## ✉️ Launch

While in the app folder, use the following command: `docker compose up --build -d`

## ✉️ Inspect

- Open API documentation in your browser at:
[swagger](http://localhost:8003/swagger/)

- Open the admin panel in your browser at: [admin_panel](http://localhost:8003/admin/)
- Login to admin panel, create and update users
```bash
login: admin
password: admin
```

