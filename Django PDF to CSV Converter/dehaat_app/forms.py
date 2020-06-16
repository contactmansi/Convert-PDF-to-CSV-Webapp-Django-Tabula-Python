from django import forms
from django.core import validators
from .models import UserInput

# Model Input form performing validations during input submission
class InputForm(forms.ModelForm):
    class Meta:
        model = UserInput
        fields = ('variable', 'year', 'input_file')

# Function to validate input files is a PDF as expected
    def clean(self):
        try:
            all_clean_data = super().clean()
            input_file = all_clean_data['input_file']
        except Exception as e:
            raise forms.ValidationError("Invalid File")

        # IF file extension is not a pdf then raises an Invalid File Extension Error during the input submission
        if(input_file.name[-3:]!= "pdf"):
            raise forms.ValidationError("Invalid File Extension: Upload a PDF EX: BalSheet.pdf")
