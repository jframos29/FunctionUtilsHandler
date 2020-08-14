import boto3
from enum import Enum
from typing import Union
from ..utils import Parser


class CommonReturnValue(Enum):
    NONE = 'NONE'


class DeleteReturnValue(CommonReturnValue, Enum):
    ALL_OLD = 'ALL_OLD'


class PutReturnValue(DeleteReturnValue, Enum):
    pass


class UpdateReturnValue(DeleteReturnValue, Enum):
    ALL_NEW = 'ALL_NEW'
    UPDATED_OLD = 'UPDATED_OLD'
    UPDATED_NEW = 'UPDATED_NEW'


DeleteReturnValueType = Union[DeleteReturnValue, CommonReturnValue]
PutReturnValueType = Union[PutReturnValue, DeleteReturnValue, CommonReturnValue]
UpdateReturnValueType = Union[UpdateReturnValue, DeleteReturnValue, CommonReturnValue]


def get_item(table_name, Key, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    return Parser.to_number(table.get_item(Key=Key, **kwargs)['Item'])


def put_item(table_name, Item, ReturnValues: PutReturnValueType = PutReturnValue.NONE, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    Item = Parser.to_decimal(Item)

    response = table.put_item(Item=Item, ReturnValues=ReturnValues.value, **kwargs)

    if ReturnValues == DeleteReturnValue.ALL_OLD:
        return Parser.to_number(response['Attributes'])


def update_item(table_name,
                Key,
                UpdateExpression,
                ExpressionAttributeValues=None,
                ReturnValues: UpdateReturnValueType = UpdateReturnValue.NONE,
                **kwargs):
    if ExpressionAttributeValues:
        ExpressionAttributeValues = Parser.to_decimal(ExpressionAttributeValues)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = Parser.to_number(
        table.update_item(
            Key=Key,
            UpdateExpression=UpdateExpression,
            ReturnValues=ReturnValues.value,
            **kwargs,
        ))

    if ReturnValues != UpdateReturnValue.NONE:
        return Parser.to_number(response['Attributes'])


def delete_item(table_name, Key, ReturnValues: DeleteReturnValueType = DeleteReturnValue.NONE, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.delete_item(Key=Key, ReturnValues=ReturnValues.value, **kwargs)

    if ReturnValues == DeleteReturnValue.ALL_OLD:
        return Parser.to_number(response['Attributes'])


def query(table_name, KeyConditionExpression, **kwargs):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.query(KeyConditionExpression=KeyConditionExpression, **kwargs)

    return Parser.to_number(response['Items']), {
        'Count': response['Count'],
        'ScannedCount': response['ScannedCount'],
        'LastEvaluatedKey': response.get('LastEvaluatedKey', None),
    }
