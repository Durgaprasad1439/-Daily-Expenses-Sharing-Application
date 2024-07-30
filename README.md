# Daily Expenses Sharing Application

This is a backend service for a daily-expenses sharing application built using Flask and SQLite. It allows users to manage their expenses, split them using various methods, and generate downloadable balance sheets.

## Features

- *User Management*: Create and manage users.
- *Expense Management*: Add and retrieve expenses, with support for different splitting methods.
- *Balance Sheet*: Generate and download a balance sheet of expenses.

## Requirements

- Python 3.7 or higher
- Flask
- Flask-SQLAlchemy
- SQLite

## Setup Instructions

### 1. Clone the Repository

Run the following command to clone the repository:

```git clone https://github.com/yourusername/daily-expenses-sharing.git```

```cd daily-expenses-sharing```
### 2. Create and Activate a Virtual Environment

Create a virtual environment and activate it:

```python -m venv venv ```

```source venv/bin/activate ```
### On Windows, use 
```venv\Scripts\activate```
### 3. Install Dependencies

Install the required Python packages:

``` pip install -r requirements.txt ```
### 4. Set Up the Database

Initialize the database and create the necessary tables:

`flask db init`

`flask db migrate`

`flask db upgrade`
### 5. Run the Application

Start the Flask development server:

```flask run```

The application will be accessible at http://127.0.0.1:5000.

## API Endpoints

### User Endpoints

- *Create User*

  - *URL*: /users
  - *Method*: POST
  - *Request Body*:
    json
    {
      "email": "user@example.com",
      "name": "User Name",
      "mobile_number": "1234567890"
    }
    

- *Retrieve User Details*

  - *URL*: /users/<int:user_id>
  - *Method*: GET

### Expense Endpoints

- *Add Expense*

  - *URL*: /expenses
  - *Method*: POST
  - *Request Body*:
    json
    {
      "description": "Expense Description",
      "total_amount": 1000,
      "date": "2024-07-29",
      "split_method": "equal",
      "created_by_id": 1,
      "splits": [
        {"user_id": 1, "amount": 500},
        {"user_id": 2, "amount": 500}
      ]
    }
    

- *Retrieve Individual User Expenses*

  - *URL*: /expenses/<int:user_id>
  - *Method*: GET

- *Retrieve Overall Expenses*

  - *URL*: /expenses/overall
  - *Method*: GET

- *Download Balance Sheet*

  - *URL*: /expenses/download
  - *Method*: GET

## Data Model

### User

- id: Integer (Primary Key)
- email: String (Unique)
- name: String
- mobile_number: String

### Expense

- id: Integer (Primary Key)
- description: String
- total_amount: Float
- date: Date
- split_method: String (e.g., "equal", "exact", "percentage")
- created_by_id: Integer (Foreign Key to User)

### ExpenseSplit

- id: Integer (Primary Key)
- user_id: Integer (Foreign Key to User)
- expense_id: Integer (Foreign Key to Expense)
- amount: Float

## Testing the API with Postman

1. *Create User*: POST request to /users
2. *Add Expense*: POST request to /expenses
3. *Retrieve Individual User Expenses*: GET request to /expenses/<user_id>
4. *Retrieve Overall Expenses*: GET request to /expenses/overall
5. *Download Balance Sheet*: GET request to /expenses/download

## Troubleshooting

- *Database Issues*: Ensure SQLite is properly configured and flask db commands are executed successfully.
- *Dependencies*: Check if all required Python packages are installed. Run pip install -r requirements.txt again if needed.
- *API Errors*: Check Flask logs for error messages and debug as necessary.

## License

This project is licensed under the MIT License.