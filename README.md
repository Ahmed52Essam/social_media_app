# Social Media API

A simple REST API for a social media application built with Python and FastAPI. This project provides basic functionalities for creating posts and commenting on them, with data stored in-memory.

## Features
- Create posts.
- Retrieve a list of all posts.
- Create comments on a specific post.
- Retrieve a list of all comments for a specific post.
- Retrieve a single post along with all of its comments.

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

## API Endpoints

Here is a summary of the available endpoints:

| Method | Path                       | Description                                |
|--------|----------------------------|--------------------------------------------|
| `POST` | `/post`                    | Creates a new post.                        |
| `GET`  | `/post`                    | Retrieves all posts.                       |
| `GET`  | `/post/{post_id}`          | Retrieves a post and all its comments.     |
| `POST` | `/comment`                 | Creates a new comment on a post.           |
| `GET`  | `/post/{post_id}/comments` | Retrieves all comments for a specific post.|

### Deactivating the Environment
When you are finished working, you can deactivate the virtual environment:
```bash
deactivate
```