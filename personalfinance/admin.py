from django.contrib import admin

from .models import Transaction, Budget, Pot
# Register your models here.
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Pot)
