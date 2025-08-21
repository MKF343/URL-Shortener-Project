URL Shortener API

A simple and efficient RESTful API built with Python and FastAPI that shortens long URLs.

---

Features

- **Shorten URLs**: Create a unique, short alias for any long URL.
- **URL Redirection**: Visiting a short URL redirects you to the original long URL.
- **Fast & Modern**: Built with FastAPI for high performance.
- **Automatic API Docs**: Interactive API documentation provided by Swagger UI.

---

Technology Stack

- **Backend**: Python 3.9+
- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy

---

Setup and Installation

To run this project locally, follow these steps:

**1. Clone the repository:**
```bash
git clone 
cd url-shortener
```

**2. Create and activate a virtual environment (optional but recommended):**
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the application:**
The server will start on `http://127.0.0.1:8000`.
```bash
uvicorn main:app --reload
```

---

API Usage

Once the application is running, you can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

### Endpoints

#### `POST /shorten`
Creates a short URL.

- **Request Body:**
  ```json
  {
    "url": "[https://www.google.com/search?q=long+url+example](https://www.google.com/search?q=long+url+example)"
  }
  ```

- **Success Response (`200 OK`):**
  ```json
  {
    "original_url": "[https://www.google.com/search?q=long+url+example](https://www.google.com/search?q=long+url+example)",
    "short_url": "[http://127.0.0.1:8000/aB1cDef](http://127.0.0.1:8000/aB1cDef)"
  }
  ```

#### `GET /{short_code}`
Redirects to the original URL.

- **Example:**
  Visiting `http://127.0.0.1:8000/aB1cDef` will redirect you to the original long URL.

- **Error Response (`404 Not Found`):**
  If the `short_code` does not exist.
  ```json
  {
    "detail": "URL not found"
  }
  ```
