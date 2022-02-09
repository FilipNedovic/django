from rest_framework import serializers
from todos.models import User, Todo
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    username = User.USERNAME_FIELD
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def validate_password(self, value):
        return make_password(value)


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'priority', 'user')
