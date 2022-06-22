from cgitb import lookup
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins
from users.filters import TransactionFilter, UserFilter
from users.models import Transaction, User
from users.serializers import TransactionSerializer, UserSerializer, UserTransactionSerializer
from rest_framework.decorators import action
from django.db.models import Q
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filterset_class = UserFilter


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Create transaction by user_email and list transactions by user_email, id and/or type
    """

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filterset_class = TransactionFilter

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(TransactionViewSet, self).create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


"""
TODO We want to be able to see a summary that shows the total inflow and total outflows per user
GET /transactions?group_by=type

[
{
"user_email": "janedoe@email.com",
"total_inflow": "2651.44",
"total_outflow": "-761.85"
},
{
"user_email": "johndoe@email.com",
"total_inflow": "0.00",
"total_outflow": "-51.13"
}
]
"""

class UserTransactionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = UserTransactionSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user_email = self.request.query_params.get("email")
        if user_email:
            return self.queryset.filter(email=user_email)
        return self.queryset

    """
    We want to be able to see a user's summary by category that shows the sum of amounts
    per transaction category:

    GET /transactions/{user_email}/summary
    {
    "inflow": {
    "salary": "2500.72",
    "savings": "150.72"
    },
    "outflow": {
    "groceries": "-51.13",
    "rent": "-560.00",
    "transfer": "-150.72"
    }
    }
    """
    @action(methods=["get"], detail=False)
    def summary(self, request, pk=None):
        user_email = self.request.query_params.get("email")
        if user_email:
            user = get_object_or_404(User, email=user_email)
            transactions = user.transaction_set.all()
        else:
            transactions = Transaction.objects.all()
        
        inflow = {}
        outflow = {}
        
        for transaction in transactions:
            if transaction.type == "inflow":
                if transaction.category not in inflow:
                    inflow[transaction.category] = 0
                inflow[transaction.category] += transaction.amount
            elif transaction.type == "outflow":
                if transaction.category not in outflow:
                    outflow[transaction.category] = 0
                outflow[transaction.category] += transaction.amount
        return Response({
            "inflow": inflow,
            "outflow": outflow
        })
        

