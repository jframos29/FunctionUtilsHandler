import boto3
from .utils import stringify_message


def enqueue_message(queue_name, message, **kwargs):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    queue.send_message(
        MessageBody=stringify_message(message),
        **kwargs,
    )
