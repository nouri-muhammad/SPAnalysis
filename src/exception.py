import sys  

from logger import logging

def error_message_details(error, error_detail):
    _, _, exc_tb = error_detail.exc_info() 
    # sys.exc_info() returns, exception type, exception value, and traceback object.
    # traceback object, shows in which file and line the error occured.
    file_name = exc_tb.tb_frame.f_code.co_filename
    # the file that error occurred in
    line_number = exc_tb.tb_lineno
    # the line that error occurred in
    error_message = f"Error occurred in python script: {file_name}\nin line {line_number}\nwith the message: {str(error)}"
    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail) -> None:
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail)

    def __str__(self):
        return self.error_message
