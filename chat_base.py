import os
from threading import Thread, Lock
from colors import red, blue, bold_blue, bold_green
from connect_four import ConnectFour


class ChatBase:
    """This is the parent class of ChatServer and ChatClient, it is not intended to be used on its own"""

    QUIT_COMMAND = '/q'
    CONNECT4_COMMAND = '/connect4'

    def __init__(self):
        self._print_lock = Lock()
        self._send_thread = Thread(target=self._send_messages)
        self._receive_thread = Thread(target=self._receive_messages)
        self._chatting = False
        self._game = None

        # These are initiated in the child classes
        self._other_source = None
        self._socket = None

    def chat(self):
        """Public method to start the send and receive threads"""
        self._chatting = True
        self._send_thread.start()
        self._receive_thread.start()
        while self._send_thread.is_alive() and self._receive_thread.is_alive():
            pass
        self._close()

    def _send_messages(self):
        """Sends messages from user input"""
        while self._chatting:
            message = input(bold_green('You:     '))
            try:
                # Message is a command
                if message[0] == '/':
                    if self._process_command(message):  # only send valid command
                        self._socket.send(message.encode())
                else:
                    self._socket.send(message.encode())

            # Unexpected disconnect
            except ConnectionResetError:
                self._print(blue(f'{self._other_source} disconnected'))
                self._chatting = False

    def _receive_messages(self):
        """Receives messages"""
        while self._chatting:
            try:
                response = self._socket.recv(4096).decode()
                if response:
                    if response[0] == '/':  # the response is a command
                        self._process_command(response, self._other_source)
                    else:
                        # Print the response
                        self._print(bold_blue(f'\r{self._other_source}: '), blue(response))
                        # Reprint the overwritten prompt
                        self._print(bold_green('You:     '), end="", flush=True)

            # Unexpected disconnect
            except ConnectionResetError:
                self._print(bold_blue(f'\r{self._other_source} disconnected'))
                self._chatting = False

            # The socket has been closed
            except OSError:
                if self._chatting:
                    self._print(bold_blue(f'\r{self._other_source} disconnected'))
                self._chatting = False

    def _process_command(self, command, source=None):
        """Processes /commands. Returns True on success"""
        # End the chat
        if command == ChatBase.QUIT_COMMAND:
            self._end_chat(source)
            return True

        # Start connect 4
        elif command == ChatBase.CONNECT4_COMMAND:
            self._begin_connect4(source)
            return True

        # Move commands for connect4
        elif len(command) == 2 and command[1] in (str(col) for col in range(7)):
            return self._connect4_move(command[1], source)

        else:
            print(red('Command not recognized'))

    def _end_chat(self, source):
        """End the chat after /q command"""
        if source == self._other_source:
            self._print(bold_blue(f'\rThe {self._other_source} ended the chat'))
        else:
            self._print(bold_green('You ended the chat'))
        self._chatting = False

    def _begin_connect4(self, source):
        """Start a new connect4 game after /connect4 command"""
        self._player_num = 1 if source == self._other_source else 2
        self._game = ConnectFour(self._player_num)

        print(bold_green(f"You are player {self._player_num}"))

        if source == self._other_source:
            self._print(bold_green('You:     '), end="", flush=True)

    def _connect4_move(self, col, source):
        """Process a connect4 move command. Returns True on success"""
        if self._game:
            if self._game.move(int(col), 3 - self._player_num if source == self._other_source else self._player_num):
                if source == self._other_source:
                    # Reprint the overwritten prompt
                    self._print(bold_green('You:     '), end="", flush=True)
                return True
        else:
            print(red(f'No active game. Send {ChatBase.CONNECT4_COMMAND} to start a new one'))

    def _print(self, *a, **b):
        """Thread safe print method"""
        with self._print_lock:
            print(*a, **b)

    def _close(self):
        """Terminates the process"""
        # This is a forced exit because input in _send_thread is blocking, so it cannot be signalled to end
        self._socket.close()
        os._exit(0)
