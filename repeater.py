"""Provide a warper for retry a function
"""


def retry(retry_times, error_handle=None):
    def retry_decorator(func):
        def func_wrapper(*args, **kwargs):
            times = 0
            while times < retry_times:
                try:
                    return func(*args, **kwargs)
                except:
                    times += 1
            if error_handle:
                error_handle()
        return func_wrapper
    return retry_decorator
