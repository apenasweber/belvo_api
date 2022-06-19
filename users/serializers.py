from rest_framework import serializers

from users.models import Transaction, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email")


class TransactionSerializer(serializers.ModelSerializer):
    # create a validator to check if decimal number is negative when type is outflow. If so, raise an error.
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
