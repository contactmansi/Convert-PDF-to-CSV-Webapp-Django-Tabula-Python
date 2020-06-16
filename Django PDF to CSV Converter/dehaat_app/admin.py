from django.contrib import admin
from dehaat_app.models import Transaction, UserInput
# Register your models here.

# Registered the Transaction and UserInput models here
admin.site.register(Transaction)
admin.site.register(UserInput)
