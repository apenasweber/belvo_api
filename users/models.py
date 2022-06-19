from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


type_choices = (
    ("inflow", "inflow"),
    ("outflow", "outflow"),
)


class Transaction(models.Model):
    reference = models.CharField(max_length=255, unique=True)
    date = models.DateField()
    type = models.CharField(max_length=255, choices=type_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    user_email = models.ForeignKey(User, to_field="email", on_delete=models.CASCADE)
    REQUIRED_FIELDS = ["reference", "date", "type", "amount", "category", "user_email"]

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
