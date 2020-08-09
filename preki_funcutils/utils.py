import json

LIST_SEPARATOR = '@@'


def stringify_message(message):
    if isinstance(message, dict):
        return json.dumps(message, ensure_ascii=False).encode('utf8')
    elif isinstance(message, list):
        return LIST_SEPARATOR.join(message)
    return str(message)


def parse_message(message):
    try:
        return json.loads(message)
    except json.decoder.JSONDecodeError:
        if LIST_SEPARATOR in message:
            return message.split(LIST_SEPARATOR)
        return message
