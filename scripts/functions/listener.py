import socket
from threading import Thread
from scripts.functions.handler import handle_event

_PORT = 1000


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', _PORT))
    serversocket.listen(5)
    print('Listening on localhost:1000...')

    while True:
        connection, address = serversocket.accept()
        buf = connection.recvmsg(1024)
        connection.close()
        if len(buf) > 0:
            t = Thread(target=handle_event, args=(buf,))
            t.start()


main()
