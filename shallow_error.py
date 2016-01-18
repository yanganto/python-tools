import sys
import traceback
import error
try:
    error.deep_error()
except:
    print(type(sys.exc_info()[1]))
    print(sys.exc_info()[1])
    print("#"*10)

    print(type(sys.exc_info()[2].tb_frame.f_code.co_filename))
    print(sys.exc_info()[2].tb_frame.f_code.co_filename)
    print("#"*10)

    print(type(sys.exc_info()[2].tb_lineno))
    print(sys.exc_info()[2].tb_lineno)
    print("#"*10)

    print(type(traceback.format_stack()))
    print(''.join(traceback.format_stack()))
    print("#"*10)
