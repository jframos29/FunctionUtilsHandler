import boto3
from .utils import parse_message


def call_lambda(function_name, payload, invocation_type='RequestResponse'):
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=function_name,
        Payload=payload,
        InvocationType=invocation_type,
    )

    return parse_message(response['Payload'].read().decode('utf-8'))
