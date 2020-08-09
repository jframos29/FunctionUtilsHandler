import boto3
from ..utils import stringify_message


def enqueue_message(queue_name, message, **kwargs):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    return queue.send_message(
        MessageBody=stringify_message(message),
        **kwargs,
    )


def enqueue_messages_batch(queue_name, messages, **kwargs):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    return queue.send_messages(
        Entries=[{
            'Id': f'{i}',
            'MessageBody': stringify_message(m)
        } for i, m in enumerate(messages)],
        **kwargs,
    )
