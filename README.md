# Social Media API

A simple REST API for a social media application built with Python and FastAPI. This project provides basic functionalities for creating posts and commenting on them, with data stored in a SQLite database.

## Features
- User registration and authentication (JWT-based).
- Email confirmation for new users sent as a background task.
- Authenticated users can create posts.
- Authenticated users can like posts.
- Authenticated users can upload files.
- Retrieve a list of all posts with sorting options (new, old, most likes).
- Authenticated users can create comments on a specific post.
- Retrieve a list of all comments for a specific post.
- Retrieve a single post along with all of its comments and like count.
- **AI Image Generation:** Automatically generate images for posts based on text prompts using the DeepAI API.


## Database

This project uses **SQLAlchemy** to interact with a **SQLite** database.

- **Database Schema:** The schema is defined in `social_media_app/database.py` and includes tables for `post`, `comments`, `users`, and `likes`.
- **Configuration:** The database connection is managed in `social_media_app/config.py` and can be configured for different environments (development, testing, production).
- **Development:** In the development environment, the application uses a `data.db` file in the project root.

## Project Analysis Summary

This project is a well-structured and feature-rich example of a modern Python backend application. It demonstrates best practices for everything from configuration and logging to testing and API design.

### Application Entrypoint (`main.py`)

The `main.py` file is the core of the application. It initializes the FastAPI application and brings together the other components.

*   **Lifespan Management:** It uses a `lifespan` context manager to connect to the database when the application starts and disconnect when it stops. This is a clean and efficient way to manage resources.
*   **Middleware:** It includes `CorrelationIdMiddleware`, which is used to add a unique ID to each request. This is invaluable for tracing requests through the system and for debugging.
*   **Routing:** It imports and includes the `post_router` from `routers/post.py`. This keeps the API routing organized and modular.
*   **Exception Handling:** It defines a custom exception handler for `HTTPException`. This handler logs the exception, which is a good practice for monitoring and debugging.

### Database Setup (`database.py`)

The `database.py` file is responsible for all database-related setup.

*   **Database URL:** It uses a `DATABASE_URL` from the `config` module to connect to the database. This allows for easy configuration for different environments.
*   **Table Definitions:** It uses SQLAlchemy's `Table` construct to define the `post` and `comments` tables. This is a direct way to define the database schema in Python.
*   **Async Database Access:** It uses the `databases` library to provide an asynchronous interface to the database. This is crucial for a high-performance FastAPI application.
*   **Forced Rollback:** It uses a `DB_FORCE_ROLL_BACK` flag from the `config` module. This is a great feature for testing, as it ensures that each test runs in a clean database state.

### Configuration (`config.py`)

The `config.py` file manages the application's configuration using Pydantic's `BaseSettings`.

*   **Environment-Based Configuration:** It defines different configuration classes for `dev`, `prod`, and `test` environments. This is a best practice for managing configuration in a real-world application.
*   **`.env` File Support:** It uses `SettingsConfigDict` to load configuration from a `.env` file. This is a standard way to manage secrets and environment-specific variables.
*   **Type-Safe Configuration:** By using Pydantic, the configuration is type-safe. This means that you get validation and type hints for your configuration variables.
*   **Caching:** It uses `lru_cache` to cache the configuration. This is a small optimization that can improve performance.

### Logging (`logging_config.py`)

The `logging_config.py` file sets up a sophisticated logging system.

*   **Structured Logging:** It uses `python-json-logger` to format logs as JSON. This is essential for modern log management systems.
*   **Log Rotation:** It uses a `RotatingFileHandler` to rotate log files. This prevents log files from growing indefinitely.
*   **Third-Party Integration:** It includes a `LogtailHandler` to send logs to the Logtail service. This is a great example of how to integrate with a third-party logging service.
*   **Email Obfuscation:** It defines a custom logging filter to obfuscate email addresses in the logs. This is a crucial security feature to prevent sensitive data from being leaked into the logs.

### API Routes (`routers/post.py`)

The `routers/post.py` file defines the API endpoints for managing posts and comments.

*   **Async Endpoints:** All the endpoints are `async` functions, which allows them to take full advantage of the asynchronous database driver.
*   **Request and Response Models:** It uses Pydantic models for request and response validation. This ensures that the API is well-documented and that the data is valid.
*   **Detailed Logging:** It includes detailed logging for each endpoint. This is very helpful for debugging and for understanding how the API is being used.
*   **Comment Management:** In addition to post management, it also includes endpoints for creating comments and for retrieving a post with its comments. This shows a more complex and realistic use case than simple CRUD.

### Data Models (`models/post.py`)

The `models/post.py` file defines the Pydantic models used in the application.

*   **Input and Output Models:** It defines separate models for input (`UserPostIn`, `CommentIn`) and output (`UserPost`, `Comment`). This is a good practice that allows for more control over the API's interface.
*   **ORM Mode:** It uses `ConfigDict(from_attributes=True)` to enable "ORM mode". This allows the Pydantic models to be created directly from SQLAlchemy objects.
*   **Nested Models:** It defines a `UserPostWithComments` model that includes a `UserPost` and a list of `Comment`s. This shows how to create complex, nested response models.

### Testing (`tests/routers/test_post.py`)

The `tests/routers/test_post.py` file contains the tests for the post and comment endpoints.

*   **Async Testing:** It uses `pytest-anyio` to write asynchronous tests. This is necessary for testing an async application.
*   **HTTPX for API Calls:** It uses `httpx.AsyncClient` to make asynchronous API calls to the application.
*   **Fixtures for Test Data:** It uses `pytest` fixtures to create test data (`created_post`, `created_comment`). This makes the tests cleaner and more reusable.
*   **Comprehensive Test Coverage:** It includes tests for creating posts and comments, getting all posts, getting comments on a post, and getting a post with its comments. It also includes tests for error conditions, such as creating a post without a body or getting a missing post.

### User Management (`routers/user.py`)

This module handles user registration and authentication.

*   **User Registration:** The `/register` endpoint creates a new user, hashes their password, and stores them in the database. It then triggers a background task to send a confirmation email.
*   **Authentication:** The `/token` endpoint implements the OAuth2 password flow. It authenticates a user and returns a JWT access token.
*   **Email Confirmation:** The `/confirm/{token}` endpoint is used to verify a user's email address using a confirmation token sent to them upon registration.

### Security (`security.py`)

This module is central to the application's security.

*   **Password Hashing:** It uses `passlib` to hash user passwords before storing them and to verify passwords during login.
*   **JWT Management:** It handles the creation and verification of JSON Web Tokens (JWTs) for both access and email confirmation purposes. It includes functions to handle token expiration and invalid tokens.
*   **Dependency Injection:** It provides a `get_current_user` dependency that can be injected into any endpoint to ensure that the request is coming from an authenticated and confirmed user.

### Background Tasks (`tasks.py`)

The `tasks.py` module offloads long-running operations to be executed in the background, ensuring the API remains responsive.

*   **Email Sending:** It contains the logic for sending emails using the Mailgun API via `httpx`. This is used to send a confirmation email to new users without blocking the registration API response.
*   **AI Image Generation:** The `generate_and_add_to_post` task uses the DeepAI API to generate an image based on a provided prompt. Once generated, it updates the post in the database and notifies the user via email.
*   **Error Handling:** It includes custom exception handling for API errors when communicating with the Mailgun or DeepAI services.


### File Upload (`routers/upload.py`)

This module is responsible for handling file uploads.

*   **Temporary Storage:** When a file is uploaded, it's first saved to a temporary location on the server.
*   **Cloud Upload:** The file is then uploaded from the temporary location to a cloud storage provider (in this case, Backblaze B2).
*   **Security:** The endpoint is protected and requires an authenticated user to be able to upload files.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Python 3.9+

### Installation

1.  **Clone the repository (optional)**
    If you have this project in a git repository, clone it first. Otherwise, just navigate to your project directory.

2.  **Create and Activate a Virtual Environment**
    It's highly recommended to use a virtual environment to manage project dependencies.

    -   **On Windows:**
        ```powershell
        # Create the virtual environment
        python -m venv venv

        # Activate the virtual environment
        .\venv\Scripts\Activate.ps1
        ```
        > **Note:** If you encounter an `UnauthorizedAccess` error in PowerShell, you may need to change the execution policy for the current process. Run the following command and then try activating the environment again:
        > ```powershell
        > Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
        > ```

    -   **On macOS / Linux:**
        ```bash
        # Create the virtual environment
        python3 -m venv venv

        # Activate the virtual environment
        source venv/bin/activate
        ```

3.  **Install Dependencies**
    With your virtual environment active, install the required packages from `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

Once the dependencies are installed, you can start the development server using Uvicorn.

```bash
uvicorn social_media_app.main:app --reload
```
- The `--reload` flag makes the server automatically restart after code changes.
- The API will be running at **http://127.0.0.1:8000**.
- You can access the interactive API documentation (Swagger UI) at **http://127.0.0.1:8000/docs**.

## Running Tests

To run the automated tests for this project, you'll first need to install the development dependencies.

1.  **Install Development Dependencies**
    With your virtual environment active, install the required packages from `requirments-dev.txt`.
    ```bash
    pip install -r requirments-dev.txt
    ```

2.  **Run Tests**
    Execute the following command to run the test suite with pytest:
    ```bash
    pytest
    ```

## API Endpoints

Here is a summary of the available endpoints. Endpoints marked with `(auth)` require a valid JWT access token.

| Method | Path                       | Description                                |
|--------|----------------------------|--------------------------------------------|
| `POST` | `/register`                | Creates a new user.                        |
| `POST` | `/token`                   | Authenticates a user and returns a token.  |
| `GET`  | `/confirm/{token}`         | Confirms a user's email address.           |
| `POST` | `/post` (auth)             | Creates a new post. Supports optional `prompt` query parameter for AI image generation. |
| `GET`  | `/post`                    | Retrieves all posts.                       |
| `GET`  | `/post/{post_id}`          | Retrieves a post and all its comments.     |
| `POST` | `/comment` (auth)          | Creates a new comment on a post.           |
| `GET`  | `/post/{post_id}/comments` | Retrieves all comments for a specific post.|
| `POST` | `/like` (auth)             | Likes a specific post.                     |
| `POST` | `/upload` (auth)           | Uploads a file.                            |

### Deactivating the Environment
When you are finished working, you can deactivate the virtual environment:
```bash
deactivate
```