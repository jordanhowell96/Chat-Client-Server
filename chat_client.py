import socket
from chat_base import ChatBase
from colors import bold_orange, red


class ChatClient(ChatBase):
    """Chat Client which inherits from ChatBase"""

    def __init__(self, host, port):
        super().__init__()
        self._socket = self._establish_connection(host, port)
        self._other_source = 'Server'

    @staticmethod
    def _establish_connection(host, port):
        """Establishes connection to the server"""

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            print(red('The server appears to be offline, could not connect'))
            exit()

        print(bold_orange(f'Connected to {host} on port {port}'))
        print(bold_orange('Send your messages at any time'))
        print(bold_orange('Send /{command} to send a command\n'))
        print(bold_orange('Available commands:\n/q :        Quit the chat\n/connect4 : Play connect four\n'))

        return sock


def main():
    client = ChatClient("127.0.0.1", 5000)
    client.chat()  # This terminates the program when finished


if __name__ == "__main__":
    main()
