from colors import red, bold_orange, orange, yellow, bold_yellow, bold_green, bold_blue


class ConnectFour:
    def __init__(self, player):
        self._board = [[' ' for _ in range(6)] for _ in range(7)]
        self._game_over = False
        self._current_player = 2
        self._this_player = player  # The player who initialized this game

        print(bold_orange(f"\r{' ' * 100}\nWELCOME TO CONNECT FOUR\n"))
        print(bold_orange("Players will take turns selecting a column they want to put their piece"))
        print(bold_orange(
            "Send / followed by the row you want to place your piece in to make your move, For example: /3"))
        print(bold_orange("You can still chat during the game"))
        print(bold_orange("The first to get four in a row wins"))
        print(orange("\nNote: Currently diagonal four in a row does not count as a win\n"))

        self._print_board()
        self._update_game_status()

    def move(self, column, player):
        """Performs a move by the player. Returns True on success"""

        # Check if the move is valid
        if self._game_over:
            print(red('The game is over!'))
            return
        elif player != self._current_player:
            print(red('Not your turn'))
            return

        try:
            # Progress the game
            row = self._board[column].index(' ')
            self._board[column][row] = self._current_player
            self._check_win()
            self._print_board()
            self._update_game_status()
            return True

        except ValueError:
            print(red('That column is full. Try again'))

    def _check_win(self):
        """Checks if the game is over. Currently only checks horizontal and vertical wins"""

        # Check vertical win
        for column in range(7):
            count = 0
            for row in range(6):
                count = count + 1 if self._board[column][row] == self._current_player else 0
                if count == 4:
                    self._game_over = True

        # Check horizontal win
        for row in range(6):
            count = 0
            for column in range(7):
                count = count + 1 if self._board[column][row] == self._current_player else 0
                if count == 4:
                    self._game_over = True

    def _print_board(self):
        """Prints the board to the console"""

        # Form the string to print
        printed_board = bold_yellow(f"\r{' ' * 100}\n{' ' * 8}CONNECT  FOUR\n") + yellow('+---' * 7 + '+\n')

        # Add each row
        for row in range(5, -1, -1):
            for column in range(7):
                piece = self._board[column][row]
                colored_piece = bold_green(str(piece)) if piece == self._this_player else bold_blue(str(piece))
                printed_board += yellow('| ') + f'{colored_piece} '
            printed_board += yellow('|\n') + yellow('+---' * 7 + '+\n')

        # Add column labels
        printed_board += bold_yellow('  ' + '   '.join(f'{col}' for col in range(7)))

        print(printed_board)

    def _update_game_status(self):
        """Prints the current status of the game and updates the current player"""

        if self._game_over:
            color = bold_green if self._current_player == self._this_player else bold_blue
            print(color(f"\nPlayer {self._current_player} won!\n"))
        else:
            self._current_player = 2 if self._current_player == 1 else 1
            if self._current_player == self._this_player:
                print(bold_green(f"\nYour turn\n"))
            else:
                print(bold_blue(f"\nPlayer {self._current_player}'s turn\n"))
