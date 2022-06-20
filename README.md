# TODO apply constraints
● A transaction reference is unique. [check]
● There are only two types of transactions: inflow and outflow.[check]
● All outflow transactions amounts are negative decimal numbers. [check]
● All inflow transactions amounts are positive decimal numbers. [check]
● We expect to receive transactions in bulk as well.[check]
● The transactions we receive could be already in our system, thus we need to avoid
duplicating them in our database.[check]

# TODO create routes
>>> USERS
● post user[check]
● get all users = api/users/ [check]
● get user by email = api/users/{email} [check]


>>> TRANSACTIONS
● post transaction[check]
● post transactions[check]
● get transactions by user_email [check]
● get transactions by user_email and type [check]

# TODO tests
TesteUserPost
- post user with name/email 200 [check]
- post with no name/email 400 [check]
- post user with existing email 400 [check]

TestUserGet
- get all users 200 [check]
- get user by email 200 [check]

TestTransactionPost
- post transaction 200 [check]
- post bulk transactions 200
- post transaction with no amount 400 [check]
- post transaction with inflow type and negative number 400 [check]
- post transaction with outflow type and positive number 400 [check]
- post transaction with existing reference 400 [check]

TestTransactionGet
- get all transactions 200 [check]
- get transaction by user_email 200 [check]
- get transactions by user_email and type 200 [check]
# TODO swagger [check]
# TODO dockerize [check]


RUN TESTS
docker-compose up -d
docker exec -it belvo_api bash
python manage.py test

RUN APPLICATION 
docker-compose up