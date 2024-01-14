class GameBoard:
    """
    Represents the game board and manages game state.
    """

    def __init__(self):
        """
        Initializes a new instance of the GameBoard class.
        """
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.num_games_count = 0
        self.num_wins_count = 0
        self.num_losses_count = 0
        self.num_ties_count = 0

    def num_games(self) -> int:
        """
        Returns the number of games played.

        Returns:
            int: The number of games played.
        """
        self.num_games_count += 1
        return self.num_games_count

    def num_wins(self) -> int:
        """
        Returns the number of wins.

        Returns:
            int: The number of wins.
        """
        self.num_wins_count += 1
        return self.num_wins_count

    def num_losses(self) -> int:
        """
        Returns the number of losses.

        Returns:
            int: The number of losses.
        """
        self.num_losses_count += 1
        return self.num_losses_count

    def num_ties(self) -> int:
        """
        Returns the number of ties.

        Returns:
            int: The number of ties.
        """
        self.num_ties_count += 1
        return self.num_ties_count

    def reset_game_board(self):
        """
        Resets the game board to its initial state.
        """
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def update_game_board(self, row: int, col: int, player: str) -> bool:
        """
        Updates the game board with the player's move.

        Args:
            row (int): The row index of the move.
            col (int): The column index of the move.
            player (str): The player's symbol ('X' or 'O').

        Returns:
            bool: True if the move was successfully made, False otherwise.
        """
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Checks if the specified player is a winner.

        Args:
            player (str): The player's symbol ('X' or 'O').

        Returns:
            bool: True if the player is a winner, False otherwise.
        """
        # Check for winning conditions
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                return True

            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True

        return False

    def board_is_full(self) -> bool:
        """
        Checks if the game board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        # Check if the game is a draw
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def compute_stats(self, num_games_element, num_wins_element, num_losses_element, num_ties_element, turn_label_element) -> str:
        """
        Computes the game statistics and updates the corresponding GUI elements.

        Args:
            num_games_element: The GUI element to display the number of games.
            num_wins_element: The GUI element to display the number of wins.
            num_losses_element: The GUI element to display the number of losses.
            num_ties_element: The GUI element to display the number of ties.
            turn_label_element: The GUI element to display the turn label.

        Returns:
            str: The statistics string in the format 'q num_games num_wins num_losses num_ties'.
        """
        num_games_element.config(text=self.num_games_count)
        num_wins_element.config(text=self.num_wins_count)
        num_losses_element.config(text=self.num_losses_count)
        num_ties_element.config(text=self.num_ties_count)
        turn_label_element.config(text="Game Over")
        return f'q {self.num_games_count} {self.num_wins_count} {self.num_losses_count} {self.num_ties_count}'
