# Apollo Test Project

This project is a Django application that logs in to a specified service, retrieves cookies, and stores request information in a database. The application allows you to send POST requests to initiate the login and data retrieval process.

## Requirements

Make sure you have the following installed:

- Python 3.x
- Django
- Selenium
- Other dependencies listed in `requirements.txt`

## Setup Instructions

Follow these steps to set up and run the project:

1. **Clone the repository**:
   ```bash
   git clone git@github.com:SergeyDev1996/ApolloTest.git
   cd ApolloTest


2. **Install requirements:**:
    ```bash
    pip install -r requirements.txt
    

3. **Run migrations:**

     Run the following command to create the necessary database tables:
    ```bash
      python manage.py migrate
      
4. **Run the server**:

    Start the Django development server:
    ```bash
    python manage.py runserver
   
5. **Send a POST request**:

    Use a tool like curl or Postman to send a POST request to the following URL:
    ```bash 
   curl -X POST http://127.0.0.1:8000/api/runapp
   ```
   You should receive a notification stating that the request has been written to the database.

