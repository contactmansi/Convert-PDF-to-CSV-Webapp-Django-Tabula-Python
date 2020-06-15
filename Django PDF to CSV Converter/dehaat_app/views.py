from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from dehaat_app.models import Transaction,UserInput
from dehaat_app.forms import InputForm
from dehaat_app.tasks import PdfConverter
from dehaat_app.tasks import parse_csv
from dehaat_app.tasks import retrieve_Amount
from dehaat_app.tasks import run_use_cases
from dehaat_app.errors import UnexpectedFile, InvalidInput
import csv
import os

# Create your views here.

def input(request):

    form = InputForm()

    if request.method == 'POST':

        form = InputForm(request.POST, request.FILES)

        if form.is_valid():

            if 'input_file' in request.FILES:
                user_input_file = request.FILES['input_file']
                input_variable = request.POST['variable'].lower()
                input_year = request.POST['year']
            else:
                return render(request,'dehaat_app/input.html', {'form':form,'error':'File Not Found : Please Upload BalSheet.pdf'})

            #Save the form data into Database defined in models.py
            form.save()

            try:
                #Call to run_use_cases(): Driver function in tasks.py to handle all use_cases
                output_dict =  run_use_cases(user_input_file,input_variable, input_year)
                return render(request,'dehaat_app/output.html', context = output_dict)

            except UnexpectedFile as e:
                return render(request,'dehaat_app/input.html', {'form':form,'error':'Unexpected file: Upload BalSheet.pdf'})
            except InvalidInput as e:
                return render(request,'dehaat_app/input.html', {'form':form,'error':'Recommend to check Variable and Year values! \n Please try again with valid inputs'})
            except Exception as e:
                return render(request,'dehaat_app/input.html', {'form':form, 'error':str(e).upper() + ': Please provide valid inputs again'})

    else:
        form = InputForm()
    return render(request,'dehaat_app/input.html', {'form':form})


def download(request, output_file_path):

    if os.path.exists(output_file_path):
        file = open(output_file_path, 'rb')
        response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(output_file_path)
        return response
    raise Http404("The Download file was not found. May have been deleted after processing")
