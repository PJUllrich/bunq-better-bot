import json
import logging

from backend.func.save import BaseHandler

logger = logging.getLogger(__name__)


class EventHandlerPlatform:
    """A callback event handling platform that receives an event, parses its
    message from bytes to JSON, and passes said message on to a previously
    registered BaseHandler sub-class"""

    HANDLERS = {}

    @classmethod
    def add_handler(cls, handler_class: BaseHandler, category):
        cls.HANDLERS[category] = handler_class

    @classmethod
    def handle_event(cls, data_bytes):
        msg_json = cls.parse_message(data_bytes)

        category = msg_json['NotificationUrl']['category']
        logger.info(f'Event received! - {category}')

        handler = cls.HANDLERS.get(category)
        if handler is None:
            logger.error(f'No handler found for category: {category}')
            return

        handler.handle_event(msg_json)

    @staticmethod
    def parse_message(data_bytes):
        """Parses an incoming data from bytes to json"""
        data_str = data_bytes.decode('UTF-8')
        data_json = json.loads(data_str)
        return data_json
