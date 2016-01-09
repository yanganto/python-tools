import sys
import traceback
import error
try:
    error.deep_error()
except:
    print(sys.exc_info()[2].tb_frame.f_code.co_filename)
    print(sys.exc_info()[2].tb_lineno)
