import abc


class BaseHandler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def handle_event(self, msg_json):
        """Handle incoming JSON data from a Callback Event
        """
