import json
import logging
from functools import wraps


class PrekiException(Exception):

    def __init__(self, message, status_code=400, error_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


def make_response(body, status_code=200):
    return {'statusCode': status_code, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(body)}


def make_error(type, message, error_code, status_code):
    error = {'type': type, 'message': message, 'error_code': error_code}
    return make_response(body={'error': error}, status_code=status_code)


def lambda_response(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return make_response(body=response)
        except PrekiException as e:
            logging.exception(e)
            return make_error(type=type(e).__name__,
                              message=e.message,
                              error_code=e.error_code,
                              status_code=e.status_code)
        except Exception as e:
            logging.exception(e)
            make_error(type=type(e).__name__, message=str(e), error_code=None, status_code=400)

    return wrapper
