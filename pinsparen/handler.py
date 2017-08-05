import json
import logging

logger = logging.getLogger(__name__)

HANDLERS = {}


def add_event_handler(category, handler_func):
    HANDLERS[category] = handler_func


def handle_event(data_bytes):
    msg_json = parse_message(data_bytes)
    category = msg_json['NotificationUrl']['category']
    logger.info(f'Event received! - {category}')

    handler = HANDLERS.get(category)
    if handler is None:
        logger.warning(f'No handler found for category: {category}')
        return

    handler(msg_json)


def parse_message(data_bytes):
    """Parses an incoming data from bytes to json"""
    data_str = data_bytes.decode('UTF-8')
    data_json = json.loads(data_str)
    return data_json
