# Belvo User Transactions API

Belvo Challenge API. Project was built with Django, DRF and Python 3.8. It uses SQLite for data persistence and ApiTestCase from DRF as testing suite. All the project was organized in a development environment so environment variables is not ommited.


## Installation and run

1. You can use docker-compose to run application and database together in root folder of project with:
```bash
docker-compose up -d
```

2. To run tests, you can use:

```bash
docker exec -it belvo_api bash 
```

```bash
python manage.py test
```
3. In console you can write "exit" to finish the application bash and proceed to next steps.

4. To access the docs of api you can access:

 - http://localhost:8000/swagger/
 - http://localhost:8000/redoc

OR if you like the old times, you can create a virtualenv to install the whole application.

```bash
# Create virtualenv
virtualenv venv

# Activate yout virtualenv
source venv/bin/activate

# Install dependencies 
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations 

# Run migrate
python manage.py migrate 

# Run tests
python manage.py test

# Run whole application
python manage.py runserver
```


## Documentation
To test the api endpoints using postman, you can insert on "body", "form-data" inserting key/value or just writing on the route something like:

    // POST
    http://localhost:8000/users/?name=Jane Doe&email=janedoe@email.com

1. Can create users in `POST /users` endpoint by receiving JSON data as the example below.

   ```json
   // POST data
   {"name": "Jane Doe", "email": "janedoe@email.com"}
   ```

2. `GET /users` can list all users, but you also can get a specific user using its email `GET /users?email=janedoe@email.com`

3. `POST /transactions` Can save user's transactions. Each transaction has: reference (unique), date, amount, type, category and user's email.

   ```json
   // Single transaction data
   {"reference": "000051", "date": "2020-01-13", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_email": janedoe@email.com}
   ```

   And you can upload them with a POST request of a list of transactions (bulk) in `POST /transactions`. This endpoint will consider only valid transactions (removing duplicates).

   ```json
   // POST bulk data
   [
     {"reference": "000051", "date": "2020-01-03", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_email": "janedoe@email.com"},
     {"reference": "000052", "date": "2020-01-10", "amount": "2500.72", "type": "inflow", "category": "salary", "user_email": "janedoe@email.com"}
     // ... 
   ]
   ```

   

4. You can get a user's transaction summary in `GET /users/<user_email>/transactions_summary` .

   ```json
   // Response
   [
      {"user_email":"janedoe@email.com","total_inflow":2500.72," total_outflow":-761.85},
      {"user_email":"janedoe@email.com","total_inflow":150.72, "total_outflow":0.0}
   ]
   ```

5. You can get a user's transactions summary by categories in `GET /users/<user_email>/transactions_by_category`

   ```json
   // Response
   {"inflow":{"salary":2500.72,"savings":150.72},"outflow":{"groceries":-51.13,"rent":-560.0,"transfer":-150.72}}
   ```


