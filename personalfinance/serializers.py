from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Budget, Pot, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        extra_kwargs = {'user': {'write_only': True}, 'date': {'error_messages': {'required': 'Please enter a valid date', 'invalid': 'Please enter a valid date.'}}}
        

    def validate(self, data):
        errors = {}

        # empty name
        if data['name'] == '':
            errors['name'] = 'Please enter a name'
        # no avatar selected
        if data['avatar'] == '':
            errors['avatar'] == 'Please select an avatar'
        # empty category
        if data['category'] == '':
            errors['category'] = 'Please select a category'
        # empty amount
        if data['amount'] == 0:
            errors['amount'] = 'Please enter an amount'
                    
        if errors:
            raise serializers.ValidationError(errors)
            
        return super().validate(data)    


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        extra_kwargs = {'user': {'write_only': True}}

    def validate(self, data):
        errors = {}
        # empty category
        if data['category'] == '':
            errors['category'] = 'Please select a category'
        # negative maximum
        if data['maximum'] < 0:
            errors['maximum'] = 'Maximum can\'t be negative'
        # empty theme
        if data['theme'] == '':
            errors['theme'] = 'Please select a theme'

        if errors:
            raise serializers.ValidationError(errors)    
            
        return super().validate(data)        


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
            
        return super().validate(data)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        errors = {}

        if len(data['password']) < 8:
            errors['password'] = 'min 8 characters'

        if len(data['username']) < 5:
            errors['username'] = 'min 5 characters'
        
        if errors:
            raise serializers.ValidationError(errors)
                
        return super().validate(data)    

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")