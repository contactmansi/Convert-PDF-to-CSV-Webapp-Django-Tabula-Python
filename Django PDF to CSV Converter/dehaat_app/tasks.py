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
    delete_Transactions()
    check_storage_success = parse_csv(output_file_path)
    if check_storage_success == True:
        output_amount = retrieve_Amount(input_variable, input_year)
    else:
        raise StorageError
    output_dict = {'output_file_path': output_file_path,
                   'output_amount':output_amount,
                   'variable':input_variable,
                   'year':input_year}

    return output_dict
# PdfConverter() : Functionality to extract table from PDF into dataframe and convert dataframeto CSV file
#   Input : Input file from POST request
#   Output : Complete path to the CSV file contaning the extracted table from PDF
def PdfConverter(user_input_file):
    # Create the complete path to media/files directory - The CSV file is saved here after generation
    files_directory = os.path.join(settings.MEDIA_ROOT, 'files')
    # Extract table from PDF into df(dataframe) using tabula.read_pdf() functionality in stream mode
    df = tabula.read_pdf(os.path.join(files_directory, user_input_file.name), stream= True, pages = 1)

    try:
        # Save extracted dataframe into a suitable variable for ease of use/code/understanding
        Extracted_df = df[0]
        # Identified the joined column due to PDF structure
        Joined_column = Extracted_df.iloc[:,2].copy()
        # Code logic to split the joined columns values
        Extracted_df.iloc[:,2][0:6] = Extracted_df.iloc[:,2][0:6].apply(lambda text: text.split(" ",1)[0])
        Extracted_df.iloc[:,3] = Joined_column[0:6].apply(lambda text: text.split(" ",1)[1] if len(text.split(" ",1))>1 else "" )
        # Splitting the dataframe column names
        split_labels = Extracted_df.columns[2].split(" ", 1)
        # Renaming the dataframe columns with expected column heading as per PDF
        Extracted_df.rename(columns = {Extracted_df.columns[2] : split_labels[0],
                               Extracted_df.columns[3] : split_labels[1],
                               Extracted_df.columns[4]: "",
                               Extracted_df.columns[5]: Extracted_df.columns[1],
                               Extracted_df.columns[6]: split_labels[0]}, inplace = True)
        # Creating the output file name from the input file with a csv extension
        output_file_name = user_input_file.name.split(".")[0]+'.csv'
        # Complete URL to the output file for generating/saving the Converted CSV file
        output_file_path = os.path.join(files_directory,output_file_name)
    # Exception raised if any other pdf file is uploaded which canot be processed for transactions
    except Exception as e:
    # Exception rendered in the views.py with Error message
        raise UnexpectedFile
    # Convert dataframe to CSV file using the complete path to the output file
    Extracted_df.to_csv (output_file_path, index = False, header=True)
    #Return the complete URL to the output CSV file
    return output_file_path

# delete_UserInputs() : Deletes the old user inputs stored in the dataframe from previous execution of the applications to avoid duplication
def delete_UserInputs():
    UserInputs = UserInput.objects.all()
    for input in UserInputs:
        input.delete()

# delete_Transactions() : Deletes old transactions stored in dtaabase form old executions of application to avoid duplication
def delete_Transactions():
    Transactions = Transaction.objects.all()
    for transaction in Transactions:
        transaction.delete()

# parse_csv() : Extracts data form the output CSV file into a dataframe and stores all transaction in database
#   Input: Complete path to CSV file to be stored in Transaction model databsed
#   Output: Returns True if storage is successful
def parse_csv(output_file_path):
    # Check successful status of storage into DB
    storage_success = False
    # Extract contents/data from CSV into dataframe
    output_df = pd.read_csv(output_file_path,header=None)
    # Column Name of the transaction description : Particulars in BalSheet
    variable_col_name = output_df[0][0]
    year1 = 0000
    year2 = 0000
    # Store the "To..." based transactions into the DB
    for (variable, amount_year1,amount_year2) in zip( output_df[0],output_df[1],output_df[2]):
        # Assign values of year1 and year2
        if(variable == variable_col_name):
           year1= amount_year1
           year2= amount_year2
        #If variable value is neither null nor 'Particulars' heading then it is a transaction description
        if(str(variable) != 'nan' and variable != variable_col_name):
           transaction1 = Transaction(particulars=variable.lower(), amount=amount_year1 ,  year=year1)
           transaction2 =  Transaction(particulars=variable.lower(), amount=amount_year2 ,  year=year2)
           transaction1.save()
           transaction2.save()
    # Store the "By..." based transactions into the DB
    for (variable,amount_year1,amount_year2) in zip(output_df[3],output_df[5],output_df[6]):
        if(variable == variable_col_name):
           year1= amount_year1
           year2= amount_year2
        if(str(variable) != 'nan' and variable != variable_col_name):
           transaction1 =  Transaction(particulars=variable.lower(), amount=amount_year1 ,  year=year1)
           transaction2 =  Transaction(particulars=variable.lower(), amount=amount_year2 ,  year=year2)
           transaction1.save()
           transaction2.save()

    storage_success = True
    # Return True to indicate successfulstorage in DB
    return storage_success

# retrieve_Amount() : Returns the transaction amount by querying the database with the input query variable and year
#   Input: Query Variable and Query Year
#   Output: Returns the amount transacted for the particulars and year combination
def retrieve_Amount(input_variable, input_year):

    try:
        output_transaction_list = Transaction.objects.filter(particulars = input_variable, year = input_year)
        # If returned QuerySet has no objects then raise an exception - Invalid Inputs
        return output_transaction_list[0].amount

    except Exception as e:
        # Query Variable and year combination returned no transaction amount value from the DB
        raise InvalidInput
    return 0
