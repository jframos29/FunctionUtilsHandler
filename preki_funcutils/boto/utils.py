import json


def stringify_message(message):
    if isinstance(message, dict) or isinstance(message, list):
        return json.dumps(message, ensure_ascii=False).encode('utf8')
    return str(message)


def parse_message(message):
    try:
        return json.loads(message)
    except Exception:
        return message
