import boto3
from .utils import parse_message, stringify_message


def call_lambda(function_name, payload, invocation_type='RequestResponse'):
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=function_name,
        Payload=stringify_message(payload),
        InvocationType=invocation_type,
    )

    payload = parse_message(response['Payload'].read().decode('utf-8'))
    return response, parse_message(payload['body'])
