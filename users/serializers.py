from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    documento = serializers.CharField()
    password = serializers.CharField()