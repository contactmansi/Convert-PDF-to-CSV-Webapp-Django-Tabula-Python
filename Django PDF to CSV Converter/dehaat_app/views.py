from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from dehaat_app.models import Transaction,UserInput
from dehaat_app.forms import InputForm
from dehaat_app.tasks import PdfConverter
from dehaat_app.tasks import parse_csv
from dehaat_app.tasks import retrieve_Amount
from dehaat_app.tasks import run_use_cases, delete_UserInputs
from dehaat_app.errors import UnexpectedFile, InvalidInput
import csv
import os

# Create your views here.

def input(request):
    # Create an InoutForm object to accept inputs from the user
    form = InputForm()
    # Check for POST request
    if request.method == 'POST':
        # Copy the query Variable and year along with input file into the form object
        form = InputForm(request.POST, request.FILES)
        # Validate form - all inputs are present, file has a pdf extension
        if form.is_valid():
            #Check for input file in the Http Request
            if 'input_file' in request.FILES:
                user_input_file = request.FILES['input_file']
                input_variable = request.POST['variable'].lower()
                input_year = request.POST['year']
            else:
                # Incase input file is not found : Render the Input form seeking the inputs again
                return render(request,'dehaat_app/input.html', {'form':form,'error':'File Not Found : Please Upload BalSheet.pdf'})

            # Deleteing the old user inputs in database stored from previous executions of the application
            delete_UserInputs()
            #Save the form data into UserInput Database defined in models.py
            form.save()

            try:
                #Call to run_use_cases(): Driver function in tasks.py to handle all use_cases consisting of business logic for all functionalities
                output_dict =  run_use_cases(user_input_file,input_variable, input_year)
                #Render the output.html page alongwith all data values in output_dict
                return render(request,'dehaat_app/output.html', context = output_dict)
            # Catch all Exceptions raised from tasks.py while running use cases
            except UnexpectedFile as e:
                # If PDF file contents differ from sample BalSheet.pdf then no queries or conversion can be performed
                return render(request,'dehaat_app/input.html', {'form':form,'error':'Unexpected file: Upload BalSheet.pdf'})
            except InvalidInput as e:
                # Query Variabe and Year were not found in the transactionslisted in input PDF file
                return render(request,'dehaat_app/input.html', {'form':form,'error':'Recommend to check Variable and Year values! \n Please try again with valid inputs'})
            except StorageError as e:
                # Error in storing CSV file into database
                return render(request,'dehaat_app/input.html', {'form':form,'error':'Unable to store transactions in database. Please try again with valid inputs'})
            except Exception as e:
                # For Any other exception display the exception message alongwith User Input form seeking inputs
                return render(request,'dehaat_app/input.html', {'form':form, 'error':str(e).split("]",1)[1] + ': Please provide valid inputs again'})
    # Until a post request is received render the Inputform() on the input.html
    else:
        form = InputForm()
    return render(request,'dehaat_app/input.html', {'form':form})

# Action/Click on Download CSV button --> routes the flow to urls.py --> Routes to download along with URL to output file
def download(request, output_file_path):

    if os.path.exists(output_file_path):
        file = open(output_file_path, 'rb')
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(output_file_path)
        return response
    raise Http404("The Download file was not found. May have been deleted after processing")
