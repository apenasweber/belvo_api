from rest_framework.response import Response
from rest_framework import viewsets, status

from users.filters import TransactionFilter, UserFilter
from users.models import Transaction, User
from users.serializers import TransactionSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filterset_class = UserFilter


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Create transaction by user_email and list transactions by id and/or type
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
