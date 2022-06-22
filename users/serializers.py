from rest_framework import serializers
from django.db.models import Sum
from users.models import Transaction, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "name")


class TransactionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data["type"] == "outflow" and data["amount"] >= 0:
            raise serializers.ValidationError(
                "Amount for outflow type needs to be negative"
            )
        elif data["type"] == "inflow" and data["amount"] <= 0:
            raise serializers.ValidationError(
                "Amount for inflow type needs to be positive"
            )
        return data
    class Meta:
        model = Transaction
        fields = "__all__"

class UserTransactionSerializer(serializers.ModelSerializer):
    total_amount_by_inflow = serializers.SerializerMethodField()
    total_amount_by_outflow = serializers.SerializerMethodField()

    def get_total_amount_by_inflow(self, obj):
        return obj.transaction_set.filter(type="inflow").aggregate(total_amount=Sum("amount"))["total_amount"]

    def get_total_amount_by_outflow(self, obj):
        return obj.transaction_set.filter(type="outflow").aggregate(total_amount=Sum("amount"))["total_amount"]
    class Meta:
        model = User
        fields = ("email", "total_amount_by_inflow", "total_amount_by_outflow")