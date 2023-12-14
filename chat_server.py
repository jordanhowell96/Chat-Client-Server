import socket
from chat_base import ChatBase
from colors import bold_orange


class ChatServer(ChatBase):
    """Chat server which inherits from ChatBase"""

    def __init__(self, host, port):
        super().__init__()
        self._establish_connection(host, port)
        self._other_source = 'Client'

    def _establish_connection(self, host, port):
        """Establish a listening socket"""

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen()
        sock.settimeout(.5)

        dots = 1
        client = None
        address = (None, None)
        while not client:
            print(bold_orange(f"\rWaiting for connection {'.' * dots + ' ' * (4 - dots)}"), end="")
            try:
                client, address = sock.accept()
            except socket.timeout:
                dots = (dots + 1) % 5

        print(bold_orange(f'\rConnected to {address[0]} on port {address[1]}'))
        print(bold_orange('Send your messages at any time'))
        print(bold_orange('Send /{command} to send a command\n'))
        print(bold_orange('Available commands:\n/q :        Quit the chat\n/connect4 : Play connect four\n'))

        self._socket = client


def main():
    server = ChatServer("127.0.0.1", 5000)
    server.chat()  # This terminates the program when finished


if __name__ == "__main__":
    main()
