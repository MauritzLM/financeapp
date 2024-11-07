from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Budget, Pot, Transaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['avatar', 'name', 'category', 'date', 'amount', 'recurring']


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['category', 'maximum', 'theme']


class PotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pot
        fields = ['name', 'target', 'total', 'theme']        