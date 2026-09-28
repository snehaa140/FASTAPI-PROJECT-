
# Lost & Found REST API

## 1. Project Description

The Lost & Found REST API is a backend application developed using FastAPI, SQLite, and SQLModel.

The purpose of this project is to provide a simple REST API for reporting, viewing, updating, and searching lost and found items.

Users can:
- Add a new lost or found item.
- View all reported items.
- View a specific item using its ID.
- Update the details or status of an item.
- Search/filter items by category.
- Track the status of an item as Lost, Found, or Returned.

The API uses SQLite as the database and SQLModel for database models and operations. FastAPI provides the REST API endpoints and automatic interactive API documentation through Swagger UI.


## 2. Technologies Used

The following technologies and tools are used in this project:

- **Python** – Programming language
- **FastAPI** – Web framework for building the REST API
- **SQLite** – Lightweight relational database
- **SQLModel** – ORM and data modeling library
- **Uvicorn** – ASGI server used to run the FastAPI application
- **Pydantic** – Used by FastAPI/SQLModel for data validation
- **Swagger UI** – Used for testing and documenting the API


## 3. Project Structure

```text
Lost-and-Found/
│
├── app.py
├── lost_found.db
├── requirements.txt
└── README.md
````

### Description of Files

* `app.py` – Contains the FastAPI application, database configuration, models, validation, and API endpoints.
* `lost_found.db` – SQLite database file created when the application starts.
* `requirements.txt` – Contains the required Python dependencies.
* `README.md` – Project documentation.

## 4. Installation Steps

### Step 1: Install Python

Make sure Python is installed on your system.

Check the Python version using:

```bash
python --version
```

or:

```bash
py --version
```

### Step 2: Create a Virtual Environment

Open the project folder in VS Code and open the terminal.

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

After activation, `(venv)` should appear at the beginning of the terminal.

### Step 3: Install Required Libraries

Install the required dependencies:

```bash
pip install fastapi uvicorn sqlmodel
```

If a `requirements.txt` file is available, install all dependencies using:

```bash
pip install -r requirements.txt
```

## 5. Command to Run the FastAPI Application

Run the application using:

```bash
uvicorn app:app --reload
```

Here:

* `uvicorn` runs the FastAPI application.
* `app` refers to the Python file `app.py`.
* `app` after the colon refers to the FastAPI application object.
* `--reload` automatically reloads the server whenever code changes are made.

After successfully running the command, the terminal will display a local server address.

## 6. Swagger UI URL

Open the following URL in a web browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI provides an interactive interface where all API endpoints can be viewed and tested directly.

## 7. Available API Endpoints

### 1. Create a New Item

**Method:** `POST`

**Endpoint:**

```text
/items
```

This endpoint is used to add a new lost or found item to the database.

Example request:

```json
{
    "title": "Mobile Phone",
    "description": "Black smartphone found near the library",
    "category": "Electronics",
    "location": "College Library",
    "reported_by": "Rahul",
    "status": "Found"
}
```

### 2. Get All Items

**Method:** `GET`

**Endpoint:**

```text
/items
```

This endpoint retrieves all lost and found items stored in the database.

### 3. Get Item by ID

**Method:** `GET`

**Endpoint:**

```text
/items/{item_id}
```

This endpoint retrieves a specific item using its unique ID.

Example:

```text
/items/1
```

If the item with the given ID does not exist, the API returns an appropriate `404 Not Found` response.

### 4. Update an Item

**Method:** `PUT`

**Endpoint:**

```text
/items/{item_id}
```

This endpoint is used to update the details of an existing item.

Example:

```text
/items/1
```

The API first checks whether the item exists. If the item does not exist, a `404 Not Found` error is returned.

### 5. Filter Items by Category

**Method:** `GET`

**Endpoint:**

```text
/items/category/{category}
```

This endpoint retrieves items belonging to a particular category.

Example:

```text
/items/category/Electronics
```

Possible categories include:

```text
Electronics
Documents
Accessories
```

If an invalid category is provided, the API returns a validation/error response instead of returning unrelated data.

## 8. Item Fields

Each item contains the following fields:

| Field         | Description                               |
| ------------- | ----------------------------------------- |
| `id`          | Unique ID of the item                     |
| `title`       | Name/title of the lost or found item      |
| `description` | Detailed description of the item          |
| `category`    | Category of the item                      |
| `location`    | Location where the item was lost or found |
| `reported_by` | Person who reported the item              |
| `status`      | Current status of the item                |

## 9. Valid Categories

The API supports categories such as:

```text
Electronics
Documents
Accessories
```

Categories are used to organize and filter lost and found items.

## 10. Valid Status Values

The API supports the following status values:

```text
Lost
Found
Returned
```

These values represent the current state of an item.

* **Lost** – The item has been reported as lost.
* **Found** – The item has been found.
* **Returned** – The item has been successfully returned to its owner.

# 11. Application Logic Explanation

## Question 1. How is the SQLite database created using create_engine()?

The SQLite database is created using SQLModel's `create_engine()` function.

The application defines a SQLite database URL and creates an engine using:

```python
engine = create_engine("sqlite:///lost_found.db")
```

The `sqlite:///lost_found.db` connection string tells SQLModel to use SQLite and create/use a database file named `lost_found.db`.

When the application starts, the tables are created using:

```python
SQLModel.metadata.create_all(engine)
```

This checks the defined SQLModel classes and creates the required database tables if they do not already exist.

Therefore, the database does not need to be manually created.

## Question 2. How is SQLModel used to store and retrieve items?

SQLModel is used to define the structure of the database table and perform database operations.

The item model contains fields such as:

```text
id
title
description
category
location
reported_by
status
```

For storing an item, a database session is created and the item is added using:

```python
session.add(item)
session.commit()
session.refresh(item)
```

For retrieving items, SQLModel queries the database through the session.

For example:

```python
items = session.exec(select(Item)).all()
```

This retrieves all the items stored in the database.

SQLModel therefore acts as the connection between the Python objects used by the application and the SQLite database.

## Question 3. How did you implement status/category filtering?

Filtering is implemented using API endpoints and database queries.

For category filtering, the API receives the category from the URL:

```text
/items/category/{category}
```

The application then searches the database for items whose category matches the requested category.

For example:

```text
/items/category/Electronics
```

returns items belonging to the Electronics category.

Status values are controlled using validation so that only valid values such as:

```text
Lost
Found
Returned
```

can be accepted.

This allows the application to maintain consistent item statuses and categories.

## Question 4. How does the API handle a non-existing item ID?

When a user requests an item using an ID, the API searches the database for that particular item.

For example:

```text
GET /items/100
```

If item ID `100` does not exist, the API raises an HTTP exception with status code `404`.

Example:

```python
raise HTTPException(
    status_code=404,
    detail="Item not found"
)
```

The client therefore receives a clear response indicating that the requested item does not exist.

This prevents the API from returning invalid or empty item data for a non-existing ID.

## Question 5. How does validation prevent invalid status values?

Validation is used to make sure that only predefined status values are accepted.

The allowed status values are:

```text
Lost
Found
Returned
```

The model validates the status field before the data is stored or processed.

For example, a value such as:

```text
Missing
```

is not an allowed status value.

Therefore, the API rejects invalid input and returns a validation error instead of storing incorrect status information in the database.

This helps maintain data consistency and ensures that the API follows the defined rules for item status.

# 12. Error Handling

The API handles common invalid requests using appropriate HTTP responses.

For example:

### Non-existing Item

If an item ID does not exist:

```text
404 Not Found
```

is returned.

### Invalid Status

If an invalid status is provided:

```text
422 Unprocessable Entity
```

may be returned by FastAPI validation.

### Invalid Input

FastAPI and SQLModel validate incoming request data and return an appropriate validation error when the supplied data does not match the expected format.

# 13. Example API Workflow

The basic workflow of the application is:

```text
User
  |
  v
FastAPI REST API
  |
  v
Request Validation
  |
  v
SQLModel
  |
  v
SQLite Database
  |
  v
Response
```

For example:

```text
POST /items
      |
      v
Validate item data
      |
      v
Create SQLModel object
      |
      v
Store item in SQLite
      |
      v
Return created item
```

# 14. Testing the API

The API can be tested using Swagger UI.

Start the application:

```bash
uvicorn app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

From Swagger UI, the following operations can be tested:

* Create an item
* Get all items
* Get an item by ID
* Update an item
* Filter items by category
* Test invalid input
* Test a non-existing item ID

# 15. Conclusion

The Lost & Found REST API provides a simple and structured way to manage lost and found item records.

FastAPI is used to create the REST API, SQLModel is used for data modeling and database operations, and SQLite is used for persistent storage.

The application also includes input validation, category filtering, status management, and error handling for non-existing items, making the API suitable for a basic Lost & Found management system.

````

### Installation steps separately

If you're submitting this project, the **actual installation process** is:

1. Open your project folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create virtual environment:
   ```bash
   python -m venv venv
````

4. Activate it:

   ```bash
   venv\Scripts\activate
   ```
5. Install libraries:

   ```bash
   pip install fastapi uvicorn sqlmodel
   ```
6. Run your application:

   ```bash
   uvicorn app:app --reload
   ```
7. Open Swagger:

   ```text
   http://127.0.0.1:8000/docs
   ```
8. Your SQLite database file `lost_found.db` will be created automatically when the application initializes the database tables.