from django_filters import rest_framework as filters

from users.models import Transaction, User


class TransactionFilter(filters.FilterSet):
    user_email = filters.CharFilter(field_name="user_email")
    category = filters.CharFilter(field_name="type")

    class Meta:
        model = Transaction
        fields = ("user_email", "type")


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(field_name="email")

    class Meta:
        model = User
        fields = ("email",)



# TODO We want to be able to see a user's summary by category that shows the sum of amounts per transaction category