# Base class for other exceptions"""
class Error(Exception):
    pass
# Excepts error for other PDF files
class UnexpectedFile(Error):
    pass
# Inputs not found in Transaction database
class InvalidInput(Error):
    pass
