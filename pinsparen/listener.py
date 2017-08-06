import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from handler.platform import EventHandlerPlatform

logger = logging.getLogger(__name__)


class RequestHandler(BaseHTTPRequestHandler):
    """The RequestHandler for handling HTTP POST REQUESTS
    """

    def do_POST(self):
        self.send_response(200)

        content_length = int(self.headers['content-length'])
        post_body = self.rfile.read(content_length)

        if len(post_body) > 0:
            # t = Thread(target=EventHandlerPlatform.handle_event,
            #            args=(post_body,))
            # t.start()
            EventHandlerPlatform.handle_event(post_body)


def start_event_listener(port):
    server = HTTPServer(('', port), RequestHandler)
    logger.info(f'Listening on localhost:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
