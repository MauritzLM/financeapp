from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Budget, Pot, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        extra_kwargs = {'user': {'write_only': True}}


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        extra_kwargs = {'user': {'write_only': True}}


class PotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pot
        fields = '__all__'
        extra_kwargs = {'user': {'write_only': True}}

    def validate(self, data):
        errors = {}
        # negative target
        if data['target'] < 0:
            errors['target'] = 'Target can\'t be negative'
        # negative total
        if data['total'] < 0:
            errors['total'] = 'Total can\'t be negative'
        # target can't be higher than total
        if data['total'] > data['target']:
            errors['value'] = 'Total can\'t be higher than target'

        if errors:
            raise serializers.ValidationError(errors)    
            
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user