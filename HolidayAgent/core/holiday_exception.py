import sys 

def handle_exception(error,error_detail:sys):
    _,_,file_exc = error_detail.exc_info()
    line_no = file_exc.tb_lineno
    file_name =file_exc.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,line_no,str(error)
    )
    return error_message
    
    
class HolidayAgentException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = handle_exception(error_message,error_detail)
        
    def __str__(self):
        return self.error_message

