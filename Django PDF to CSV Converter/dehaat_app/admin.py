from django.contrib import admin
from .models import Transaction, UserInput
# Register your models here.

# Registered the Transaction and UserInput models here


class UserInputAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Query Information', {'fields': ['variable', 'year']}),
        ('Uploaded file',               {'fields': ['input_file']}),
    ]
    list_display = ('variable', 'year', 'input_file')


admin.site.register(UserInput, UserInputAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'particulars', 'year', 'amount')


admin.site.register(Transaction, TransactionAdmin)
