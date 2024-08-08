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

## Database Initialization
For local testing or development purposes, seed the database with `docker compose exec web python manage.py seed_db`
The database will be seeded with:
	- a `Google` social application to be used for OAuth (using credentials provided in `.env`)
	- a superuser to be used on `/admin/`	  
		username: `admin`  
		password: `password123`  
	- two users:
		- CRM admin user  
			username: `admin_user`  
			password: `password123`  
		- CRM normal user  
			username: `normal_user`  
			password: `password123`
	- a few customers

# OAuth
We will be using Google as a third party OAuth provider
* set social app in django admin * set callback url
* SUPPLY test user email in order to add to the oauth consent screen test users on google cloud console
* Set redirect URL in Google Cloud Console and in `settings.py`
* Deployment create social application in `/admin/`
* Define the redirect URL as the same as where you start your server e.g. http://127.0.0.1.
	- Set this value to `GOOGLE_REDIRECT_URL` in `settings.py`
	- Add it as a redirect URI in Authorized Javascript origins and Authorized redirect URIs in your Project in the Oauth Credential in the Google Developer console.

* To login via Google OAuth:
	Fill in:
	```
	<CALLBACK_URL_YOU_SET_ON_GOOGLE> e.g. http://127.0.0.1.
	<YOUR CLIENT ID> Google OAuth Client
	```
	Into, and navigate to it:
	`https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=<CALLBACK_URL_YOU_SET_ON_GOOGLE>&prompt=consent&response_type=code&client_id=<YOUR CLIENT ID>&scope=openid%20email%20profile&access_type=offline`

* If testing manually, after the redirection:
	- Copy the `code` part from the url query string (decode as it is URL encoded)
	- POST to `/api/rest-auth/google`. The body of the POST must have a key called `code` with the value from the previous step.
	A user will be created/logged in and an authorization token, returned.


* Create a new project and set up Google OAuth credentials in Google Cloud Console (https://console.cloud.google.com/) and copy:
	* Copy `Client ID` into `GOOGLE_OAUTH_CLIENT_ID` of `.env` file
	* Copy `Client Secret` into `GOOGLE_OAUTH_CLIENT_SECRET` of `.env` file

   - Set the authorized JavaScript origins to your frontend URL (e.g., http://localhost:3000 for development)
   - Set the authorized redirect URIs to your backend URL followed by the callback path (e.g., http://localhost:8000/accounts/google/login/callback/)
   - Note down the Client ID and Client Secret

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

## Notes on extra requirements

* ✅ README file with a getting started guide. 
* ✅ Tests implemented for the solution.
* ✅ Making project set-up for newcomers.
* ✅ The application follows the twelve-factor app principles (https://12factor.net) in order for it to be scalable.
* ✅ Follow OAuth 2 protocol for authentication (You can use a third party public OAuth provider).
* ⚠️  (incomplete) The project is ready for Continuous Deployment using a provider (e.g. AWS).
* ✅ The project uses Docker, Vagrant or other tools to make it easier to configure development environments.
