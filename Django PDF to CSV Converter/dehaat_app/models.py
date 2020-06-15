from django.db import models
from django.conf import settings
import os
# Create your models here.

class UserInput(models.Model):
    variable = models.CharField(max_length = 100)
    year = models.IntegerField(blank = True)
    input_file = models.FileField(upload_to='files/')

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    particulars = models.CharField(max_length = 100)
    year = models.IntegerField()
    amount = models.DecimalField(decimal_places = 3, max_digits = 10)

    def savedata(self):
        self.save()

    def __str__(self):
        return self.particulars+" "+str(self.year)+" "+str(self.amount)
