from django import forms
from django.core import validators
from .models import UserInput

class InputForm(forms.ModelForm):
    class Meta:
        model = UserInput
        fields = ('variable', 'year', 'input_file')

    def clean(self):

        all_clean_data = super().clean()
        year = all_clean_data['year']
        input_file = all_clean_data['input_file']

        if(input_file.name[-3:]!= "pdf"):
            raise forms.ValidationError("Invalid File Extension: Upload a PDF EX: BalSheet.pdf")
