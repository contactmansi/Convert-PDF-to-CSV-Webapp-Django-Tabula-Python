"""
TASKS.PY : Business Logic to handle the following use cases:
1. Convert the Uploaded PDF file into a CSV fie
2. Parse CSV file to store all transactions into the database - defined in models.py
3. Retrieves/Fetches the amount/value corresponding to query Variable and year
4. Return the results/putputs to views.py as an Output dictionary
"""

from dehaat_app.models import Transaction,UserInput
from django.conf import settings
from dehaat_app.errors import UnexpectedFile
from dehaat_app.errors import InvalidInput
from datetime import datetime
import pandas as pd
import numpy as np
import tabula
import sys
import os

#RUN_USE_CASES() : DRIVER FUNCTION TO RUN ALL THE USE CASES
#    Inputs from views.py: User Uploaded file, User input query variable, User input query year
#    Output to views.py: All variables rendered by output.html as a result

def run_use_cases(user_input_file,input_variable, input_year):

    output_file_path = PdfConverter(user_input_file)
    clear_Transactions()
    parse_csv(output_file_path)
    output_amount = retrieve_Amount(input_variable, input_year)
    output_dict = {'output_file_path': output_file_path,
                   'output_amount':output_amount,
                   'variable':input_variable,
                   'year':input_year}
    return output_dict

def PdfConverter(user_input_file):

    files_directory = os.path.join(settings.MEDIA_ROOT, 'files')

    df = tabula.read_pdf(os.path.join(files_directory, user_input_file.name),stream= True, pages = 1)
    try:
        Extracted_df = df[0]

        Joined_column = Extracted_df.iloc[:,2].copy()

        Extracted_df.iloc[:,2][0:6] = Extracted_df.iloc[:,2][0:6].apply(lambda text: text.split(" ",1)[0])
        Extracted_df.iloc[:,3] = Joined_column[0:6].apply(lambda text: text.split(" ",1)[1] if len(text.split(" ",1))>1 else "" )

        split_labels = Extracted_df.columns[2].split(" ", 1)

        Extracted_df.rename(columns = {Extracted_df.columns[2] : split_labels[0],
                               Extracted_df.columns[3] : split_labels[1],
                               Extracted_df.columns[4]: "",
                               Extracted_df.columns[5]: Extracted_df.columns[1],
                               Extracted_df.columns[6]: split_labels[0]}, inplace = True)

        output_file_name = user_input_file.name.split(".")[0]+'.csv'
        output_file_path = os.path.join(files_directory,output_file_name)

    except Exception as e:
        raise UnexpectedFile
    # Convert dataframe to CSV file
    Extracted_df.to_csv (output_file_path, index = False, header=True)
    #Return the complete URL to the output CSV file
    return output_file_path

def clear_UserInputs():
    UserInputs = UserInput.objects.all()
    for input in UserInputs:
        input.delete()

def clear_Transactions():
    Transactions = Transaction.objects.all()
    for transaction in Transactions:
        transaction.delete()


def parse_csv(output_file_path):

    output_file=pd.read_csv(output_file_path,header=None)

    variable_col_name = output_file[0][0]
    year1 = 0000
    year2 = 0000
    for (variable, amount_year1,amount_year2) in zip( output_file[0],output_file[1],output_file[2]):
        # Assign values of year1 and year2
        if(variable == variable_col_name):
           year1= amount_year1
           year2= amount_year2
        #If variable value is neither null nor 'Particulars' heading then it is a transaction description/variable
        if(str(variable) != 'nan' and variable != variable_col_name):
           transaction1 = Transaction(particulars=variable.lower(), amount=amount_year1 ,  year=year1)
           transaction2 =  Transaction(particulars=variable.lower(), amount=amount_year2 ,  year=year2)
           transaction1.save()
           transaction2.save()

    for (variable,amount_year1,amount_year2) in zip(output_file[3],output_file[5],output_file[6]):
        if(variable == variable_col_name):
           year1= amount_year1
           year2= amount_year2
        if(str(variable) != 'nan' and variable != variable_col_name):
           transaction1 =  Transaction(particulars=variable.lower(), amount=amount_year1 ,  year=year1)
           transaction2 =  Transaction(particulars=variable.lower(), amount=amount_year2 ,  year=year2)
           transaction1.save()
           transaction2.save()

def retrieve_Amount(input_variable, input_year):

    try:
        output_transaction_list = Transaction.objects.filter(particulars = input_variable, year = input_year)
        return output_transaction_list[0].amount

    except Exception as e:
        raise InvalidInput
    return 0
