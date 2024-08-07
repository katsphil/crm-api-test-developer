# CRM API

This is a Django REST API for managing customer data in a small shop CRM system.
Consumers of the API should consult the [Usage](#usage) section.
Developers should consult with the [Setup](#setup) and [Development](#development) sections.

## Table of Contents
- [Setup](#setup)
- [Development](#development)
- [Scripts](#scripts)
- [Deployment](#deployment)
- [Usage](#usage)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/katsphil/crm-api-test-developer.git
   cd crm-api-test-developer
   ```

2. Set up the environment:
   - Copy `.env.sample` to `.env` and adjust the values as needed:
     ```
     cp .env.sample .env
     ```
   - Edit `.env` and set the necessary environment variables.

3. Build and run with Docker:
   ```
   docker compose build
   docker compose up -d
   ```

4. Run migrations:
   ```
   docker compose exec web python manage.py migrate
   ```

5. Create a superuser:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

6. Sign in as admin (use credentials just created) to create a user and set `is_admin` to true:
   - Navigate to `http://localhost:8000/admin/`

7. Browse API:
   - Navigate to `http://localhost:8000/api/swagger/`

## Development

If you want to develop without docker, follow these steps.

1. Activate the virtual environment:
   ```
   poetry shell
   ```

2. Install dependencies:
   ```
   poetry install
   ```

3. Run the development server:
   ```
   python manage.py runserver
   ```

### Adding Dependencies

To add a new package dependency:
```
poetry add <package name>
```
You will need to rebuild the docker image in this case.

### Database Changes

If you change the models:
1. Make migrations:
   ```
   python manage.py makemigrations
   ```
2. Apply migrations:
   ```
   python manage.py migrate
   ```

### Django Shell

To access the Django shell with additional utilities:
```
docker compose exec web python manage.py shell_plus
```

## Deployment

1. Ensure your `.env` file is properly configured for production, for example:
   ```
   SECRET_KEY='secret_key'
   DEBUG=0
   ALLOWED_HOSTS=crmapi.com,www.crmapi.com
   ```

2. Set CORS appropriately in `settings.py`

3. Build and run the Docker containers:
   ```
   docker compose -f docker-compose.prod.yml up -d
   ```

4. Run migrations:
   ```
   docker compose -f docker-compose.prod.yml exec web python manage.py migrate
   docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic
   ```

## Usage

In order to interact with the API, visit `/api/swagger/`

1. Authenticate:
   - Use the `/api/rest-auth/login/` endpoint to obtain an authentication token.
   - Include the token in the Authorization header of your requests: `Authorization: Token <your_token>`

2. API Endpoints:
   - There are endpoints for `customers`, `users`, `authorization`. Visit `http:/localhost:8000/api/swagger/`

3. Admin Interface:
   - Access the admin interface at `/admin/` to manage users and customers.

## Dependencies

* **django**: The core web framework for building the application, providing essential functionality for routing, ORM, templates, and more.
* **djangorestframework**: Toolkit for building Web APIs in Django, simplifying the process of creating RESTful interfaces.
* **sqlite3**: Simple DB for local development.
* **drf-yasg**: Generates real Swagger/OpenAPI 2.0 specifications from a Django Rest Framework API.
* **python-dotenv**: Loads environment variables from a .env file, allowing for easy configuration management and separation of sensitive data from code.
* **django-cors-headers**: Adds Cross-Origin Resource Sharing (CORS) headers to responses, enabling the API to be accessed from different domains.
* **django-allauth**: Provides a set of Django applications for handling authentication, registration, and account management, including social account integration.
* **dj-rest-auth**: Offers a set of REST API endpoints for authentication and registration, working well with django-allauth for a complete auth solution.
* **django-extensions**: Adds a collection of custom extensions for Django, including management commands and additional debugging tools.
* **pillow**: Python Imaging Library fork, necessary for image processing in Django, often used for ImageField in models.
* **django-cleanup**: Automatically deletes files for FileField, ImageField, and subclasses, helping to manage file storage and prevent orphaned files.

## Things to add

* deploy to AWS
* OAuth
* production docker
* script for auto setup (setup section)
* seed_db.py script to seed DB with fake data and a superuser
* logging
* pagination & ordering
* limit image size during upload
* pre-commit + ruff for linting, formatting
    ```
    poetry add pre-commit ruff
    ```
    ```
    # .pre-commit-config.yaml
    repos:
      - repo: https://github.com/charliermarsh/ruff-pre-commit
        rev: v0.0.291
        hooks:
          - id: ruff
    ```

# Notes
* ✅ README file with a getting started guide. 
* ✅ Tests implemented for the solution.
* ✅ Making project set-up for newcomers.
* ✅ The application follows the twelve-factor app principles (https://12factor.net) in order for it to be scalable.
* ⚠️  (incomplete) Follow OAuth 2 protocol for authentication (You can use a third party public OAuth provider).
* ⚠️  (incomplete) The project is ready for Continuous Deployment using a provider (e.g. AWS).
* ✅ The project uses Docker, Vagrant or other tools to make it easier to configure development environments.
* All API endpoints require authentication through Token Authentication.
* SQL injection and XSS prevention are handled by Django's ORM and template system (not used).
* Admin user can manage other users through the Django admin interface.
* Image uploads are managed through Django's ImageField, which handles file uploads. djang-cleanup provides facilities to remove files when no longer needed.
