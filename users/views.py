from rest_framework import viewsets
from users.serializers import UserSerializer, TransactionSerializer
from users.models import User, Transaction
"""
USER MODEL
id
name
email
age
created_at

USER_TRANSACTION MODEL
reference
account
date
ammount
type
category
user_id(FK user.id)
created_at

ENDPOINTS:
create user
get user
get all users
save transaction
post transactions
get transactions by user
get transactions by user and category
"""
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    