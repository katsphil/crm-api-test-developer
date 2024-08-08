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

5. Seed database with test data (see Database Initialization) :
   ```
   docker compose exec web python manage.py seed_db
   ```

6. Sign in as admin (see Database Initialization):
   - Navigate to `http://localhost:8000/admin/`

7. Browse API:
   - Navigate to `http://localhost:8000/api/swagger/`

## Database Initialization

### Local Testing or Development
For local testing or development purposes, you can seed the database with sample data by running the following command:

```
docker compose exec web python manage.py seed_db
```

This will seed the database with the following:

1. A `Google` social application to be used for OAuth, using the credentials provided in the `.env` file.
2. A superuser account with the following credentials:
   - Username: `admin`
   - Password: `password123`
3. Two CRM user accounts:
   - CRM admin user:
     - Username: `admin_user`
     - Password: `password123`
   - CRM normal user:
     - Username: `normal_user`
     - Password: `password123`
4. A few customer records.

This seeding process helps you get started with a pre-populated database for local testing and development purposes.

## OAuth
This project integrates Google OAuth authentication to allow users to sign in using their Google accounts.

## Setup

### Django Configuration
1. Set up a social application in the Django admin panel.
2. Configure the callback URL in the Django settings (`GOOGLE_REDIRECT_URL`).
3. Ensure that the redirect URL matches the one set in the Google Cloud Console.

### Google Cloud Console Configuration
1. Create a new project in the Google Cloud Console (https://console.cloud.google.com/).
2. Set up the Google OAuth credentials:
   - Copy the `Client ID` into the `GOOGLE_OAUTH_CLIENT_ID` environment variable.
   - Copy the `Client Secret` into the `GOOGLE_OAUTH_CLIENT_SECRET` environment variable.
   - Set the authorized JavaScript origins to your frontend URL (e.g., `http://localhost:3000` for development).
   - Set the authorized redirect URIs to your backend URL followed by the callback path (e.g., `http://localhost:8000/accounts/google/login/callback/`).

### Manual Testing
1. To log in via Google OAuth, use the following URL:
   ```
   https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=<CALLBACK_URL_YOU_SET_ON_GOOGLE>&prompt=consent&response_type=code&client_id=<YOUR_CLIENT_ID>&scope=openid%20email%20profile&access_type=offline
   ```
   Replace `<CALLBACK_URL_YOU_SET_ON_GOOGLE>` with the callback URL you configured in the Django settings, and `<YOUR_CLIENT_ID>` with the Google OAuth Client ID.
2. After the redirection, copy the `code` part from the URL query string (decoded, as it is URL encoded).
3. POST the `code` to the `/api/rest-auth/google` endpoint. The body of the POST must have a key called `code` with the value from the previous step.
4. A user will be created/logged in, and an authorization token will be returned.

## Deployment
1. Create a social application in the Django admin panel.
2. Ensure that the redirect URL in the Django settings (`GOOGLE_REDIRECT_URL`) matches the one set in the Google Cloud Console.

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

## Commits

* Run `pre-commit install` in order to automatically have your code linted and
    formatted before commiting.

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

## Usage

In order to interact with the API, visit `/api/swagger/`

1. Authenticate:
   - Use the `/api/rest-auth/login/` endpoint to obtain an authentication token. (You may need to create an admin user via the admin panel. See 3)
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
* **drf-yasg**: Generates real Swagger/OpenAPI 2.0 specifications from a Django Rest Framework API.
* **pre-commit**: A framework for managing pre-commit hooks.
* **ruff**: Python linter, focuses on performance and type checking.

## Notes on extra requirements

* ✅ README file with a getting started guide. 
* ✅ Tests implemented for the solution.
* ✅ Making project set-up for newcomers.
* ✅ The application follows the twelve-factor app principles (https://12factor.net) in order for it to be scalable.
* ✅ Follow OAuth 2 protocol for authentication (You can use a third party public OAuth provider).
* ⚠️  (incomplete) The project is ready for Continuous Deployment using a provider (e.g. AWS).
* ✅ The project uses Docker, Vagrant or other tools to make it easier to configure development environments.
* All API endpoints require token authentication.
* SQL injection and XSS prevention are handled by Django's ORM and template system (not used).
* The admin superuser can manage other users through the Django admin interface.
* Image uploads are managed through Django's ImageField, which handles file uploads. django-cleanup provides facilities to remove files when no longer needed.
* Tests for third party libraries, have not been created assuming that they have been thoroughly tested already. Tests bypass e.g. third-party authentication mechanisms in order to test the actual functionality.
