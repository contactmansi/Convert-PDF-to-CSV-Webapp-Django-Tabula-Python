from django.contrib import admin
from .models import Transaction, UserInput
# Register your models here.

# Registered the Transaction and UserInput models here


class UserInputAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Query Information', {'fields': ['variable', 'year']}),
        (None,               {'fields': ['input_file']}),
    ]
    list_display = ('variable', 'year', 'input_file')


admin.site.register(UserInput, UserInputAdmin)
admin.site.register(Transaction)
