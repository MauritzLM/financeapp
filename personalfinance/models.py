from django.db import models
from django.contrib.auth.models import User


# transaction model
class Transaction(models.Model):
    avatar = models.TextField()
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    date = models.DateTimeField('Transaction Date')
    amount = models.IntegerField()
    recurring = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Transactions')

    def __str__(self):
        return self.name


# budget model
class Budget(models.Model):
    category = models.CharField(max_length=50)
    maximum = models.FloatField()
    theme = models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Budgets')

    def __str__(self):
        return self.category


# pot model
class Pot(models.Model):
    name = models.CharField(max_length=50)
    target = models.IntegerField()
    total = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Pots')
    theme = models.CharField(max_length=7)

    def __str__(self):
        return self.name

