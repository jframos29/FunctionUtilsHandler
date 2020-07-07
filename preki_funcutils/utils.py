import json
import logging
from functools import wraps
from . import status, exceptions


def _make_response(body, status_code=status.HTTP_200_OK):
    return {'statusCode': status_code, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(body)}


def _make_error(type, message, error_code, status_code):
    error = {'type': type, 'message': message, 'error_code': error_code}
    return _make_response(body={'error': error}, status_code=status_code)


def lambda_response(func):

    @wraps(func)
    def wrapper(event, context, *args, **kwargs):
        try:
            event['body'] = json.loads(event.get('body', None) or '{}')
            event['queryStringParameters'] = event.get('queryStringParameters', None) or {}
            event['pathParameters'] = event.get('pathParameters', None) or {}

            response = func(event, context, *args, **kwargs)
            return _make_response(body=response)
        except exceptions.PrekiException as e:
            logging.warning(e)
            return _make_error(type=type(e).__name__,
                               message=e.message,
                               error_code=e.error_code,
                               status_code=e.status_code)
        except Exception as e:
            logging.exception(e)
            return _make_error(type=type(e).__name__,
                               message=str(e),
                               error_code=None,
                               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper
