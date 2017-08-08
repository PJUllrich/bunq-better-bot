import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

from psparen.handler.platform import EventHandlerPlatform

logger = logging.getLogger(__name__)


class RequestHandler(BaseHTTPRequestHandler):
    """The RequestHandler for handling HTTP POST REQUESTS
    """

    def do_POST(self):
        self.send_response(200)

        content_length = int(self.headers['content-length'])
        post_body = self.rfile.read(content_length)

        if len(post_body) > 0:
            EventHandlerPlatform.handle_event(post_body)


def start_event_listener(port):
    """
    Calls a HTTPServer to connect to a specified port and sets up
    RequestHandler as an HTTP request handler.

    Args:
        port: int, the port to which the listener connects to

    """
    server = HTTPServer(('', port), RequestHandler)
    logger.info(f'Listening on localhost:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
