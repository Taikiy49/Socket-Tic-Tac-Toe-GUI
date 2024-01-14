import socket
import tkinter as tk
from gameboard import GameBoard

class TicTacToeServer:
    """
    Tic Tac Toe server class for hosting the game and managing the GUI.
    """

    def __init__(self):
        """
        Initialize the TicTacToeServer class.
        """
        self.server_socket = None
        self.client_socket = None
        self.window = None
        self.buttons = []
        self.start_button = None
        self.game_board = GameBoard()
        self.setup_window()
        self.create_buttons()

    def send(self, message: str):
        """
        Send a message to the client.

        Args:
            message (str): The message to send.
        """
        self.client_socket.send(message.encode())

    def recv(self) -> str:
        """
        Receive a message from the client.

        Returns:
            str: The received message.
        """
        data = self.client_socket.recv(1024).decode()
        return data

    def get_host_port(self) -> tuple[str, int]:
        """
        Get the host and port entered by the user.

        Returns:
            tuple[str, int]: The host and port.
        """
        host = self.host_entry.get()
        port = self.port_entry.get()
        return host, int(port)

    def connect_to_server(self):
        """
        Connect to the Tic Tac Toe server.
        """
        try:
            host, port = self.get_host_port()
            self.connect_button.config(state=tk.DISABLED)
            self.turn_label.config(text="Waiting for connection...")
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.window.update()
            self.server_socket.listen(1)
            self.client_socket, addr = self.server_socket.accept()
            self.turn_label.config(text="Connected! Waiting for Player 1 to enter their username...")
            self.window.update()
            self.game()
        except Exception:
            self.turn_label.config(text="Invalid host and port. Try again.")
            self.connect_button.config(state=tk.NORMAL)

    def setup_window(self):
        """
        Set up the GUI window for the server.
        """
        self.turn = None
        self.window = tk.Tk()
        self.window.title("Taiki's Tic Tac Toe - Player 2")
        self.window.resizable(False, False)

        # Host entry
        host_label = tk.Label(self.window, text="Host: ", font=('Arial', 12))
        host_label.grid(row=0, column=0, sticky=tk.W)
        self.host_entry = tk.Entry(self.window, font=('Arial', 10))
        self.host_entry.grid(row=0, column=1, sticky=tk.W)
        self.host_entry.config(state=tk.NORMAL)

        # Port entry
        port_label = tk.Label(self.window, text="Port: ", font=('Arial', 12))
        port_label.grid(row=1, column=0, sticky=tk.W)
        self.port_entry = tk.Entry(self.window, font=('Arial', 10))
        self.port_entry.grid(row=1, column=1, sticky=tk.W)
        self.port_entry.config(state=tk.NORMAL)

        # Connect button
        self.connect_button = tk.Button(self.window, text="Connect", font=('Arial', 12), command=self.connect_to_server)
        self.connect_button.grid(row=2, column=2, sticky=tk.E)

        # Game label
        label = tk.Label(self.window, text="Taiki's Tic Tac Toe", font=('Arial', 20))
        label.grid(row=2, columnspan=3, pady=10)

        # Game buttons
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.window, text=' ', font=('Arial', 20), width=8, height=4,
                                   command=lambda row=i, col=j: self.handle_move(row, col))
                button.grid(row=i+3, column=j)
                self.buttons.append(button)

        # Turn label
        self.turn_label = tk.Label(self.window, text=f"Please enter host and port.", font=('Arial', 14))
        self.turn_label.grid(row=6, columnspan=3, pady=10)

        # Username label
        username_label = tk.Label(self.window, text="Username: ", font=('Arial', 16))
        username_label.grid(row=7, column=0, sticky=tk.W)
        self.username_label = tk.Label(self.window, text="Player 2", font=('Arial', 16))
        self.username_label.grid(row=7, column=1, sticky=tk.W)

        # Opponent label
        opponent_label = tk.Label(self.window, text="Opponent: ", font=('Arial', 16))
        opponent_label.grid(row=8, column=0, sticky=tk.W)
        self.username_label_opponent = tk.Label(self.window, text="", font=('Arial', 16))
        self.username_label_opponent.grid(row=8, column=1, sticky=tk.W)

        # Stats
        games = tk.Label(self.window, text="Games: ", font=('Arial', 16))
        games.grid(row=9, column=0, sticky=tk.W)
        self.num_games = tk.Label(self.window, text="", font=('Arial', 16))
        self.num_games.grid(row=9, column=1, sticky=tk.W)
        wins = tk.Label(self.window, text="Wins: ", font=('Arial', 16))
        wins.grid(row=10, column=0, sticky=tk.W)
        self.num_wins = tk.Label(self.window, text="", font=('Arial', 16))
        self.num_wins.grid(row=10, column=1, sticky=tk.W)
        losses = tk.Label(self.window, text="Losses: ", font=('Arial', 16))
        losses.grid(row=11, column=0, sticky=tk.W)
        self.num_losses = tk.Label(self.window, text="", font=('Arial', 16))
        self.num_losses.grid(row=11, column=1, sticky=tk.W)
        ties = tk.Label(self.window, text="Ties: ", font=('Arial', 16))
        ties.grid(row=12, column=0, sticky=tk.W)
        self.num_ties = tk.Label(self.window, text="", font=('Arial', 16))
        self.num_ties.grid(row=12, column=1, sticky=tk.W)
        blank = tk.Label(self.window)
        blank.grid(row=13, column=1, sticky=tk.W)

        self.disable_buttons()  # Disable buttons initially

        self.window.update()

    def create_buttons(self):
        """
        Create the game buttons and reset the game board.
        """
        for button in self.buttons:
            button.config(text=' ')
        self.game_board.reset_game_board()

    def handle_move(self, row: int, col: int):
        """
        Handle a move made by the player.

        Args:
            row (int): The row index of the button.
            col (int): The column index of the button.
        """
        while self.turn:
            if self.game_board.update_game_board(row, col, 'O'):
                button = self.buttons[row * 3 + col]
                button.config(text='O', state=tk.DISABLED)
                self.turn_label.config(text=f"{self.username} is making a move...")
                self.window.update()
                self.client_socket.send(f"{row}{col}".encode())
                self.turn = False

                if self.game_board.is_winner('O'):
                    self.show_message("\n\n" + f"Player 2 wins!" + "\n" + f"{self.username} is making a decision...")
                    return

                if self.game_board.board_is_full():
                    self.show_message("\n\n" + f"Board is full!" + "\n" + f"{self.username} is making a decision...")
                    return

        while not self.turn:
            move = self.recv()
            self.game_board.update_game_board(int(move[0]), int(move[1]), 'X')
            button = self.buttons[int(move[0]) * 3 + int(move[1])]
            button.config(text='X', state=tk.DISABLED)
            self.turn_label.config(text="Player 2, please make your move.")
            self.window.update()
            self.turn = True

            if self.game_board.is_winner('X'):
                self.show_message("\n\n" + f"{self.username} wins!" + "\n" + f"{self.username} is making a decision...")
                return

            if self.game_board.board_is_full():
                self.show_message("\n\n" + f"Board is full!" + "\n" + f"{self.username} is making a decision...")
                return

    def show_message(self, message: str):
        """
        Show a message in a popup window.

        Args:
            message (str): The message to display.
        """
        self.create_buttons()
        self.disable_buttons()  # Disable buttons before displaying the popup window

        popup = tk.Toplevel()
        popup.title("Game Over")
        self.turn_label.config(text="Game Over")
        popup.geometry("300x200")
        label = tk.Label(popup, text=message, font=('Arial', 16))
        label.pack(pady=20)
        self.window.update()

        choice = self.recv()

        if choice == "play_again":
            self.turn_label.config(text=f"Play Again! {self.username} is making a move...")
            popup.destroy()
            self.create_buttons()
            self.window.update()
            self.first_move()

        elif choice[0] == "q":
            choice = choice.split()
            popup.destroy()
            self.create_buttons()
            self.num_games.config(text=choice[1])
            self.num_wins.config(text=choice[3])
            self.num_losses.config(text=choice[2])
            self.num_ties.config(text=choice[4])
            self.turn_label.config(text=f"Fun Times")
            self.server_socket.close()
            self.window.update()

    def disable_buttons(self):
        """Disable all game buttons."""
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def enable_buttons(self):
        """Enable all game buttons."""
        for button in self.buttons:
            button.config(state=tk.NORMAL)

    def game(self):
        """Start the game."""
        self.username = self.recv()
        self.username_label_opponent.config(text=self.username)
        self.enable_buttons()
        self.turn_label.config(text=f"{self.username} is making a move...")
        self.window.update()
        self.first_move()

    def first_move(self):
        """Handle the first move of the game."""
        move = self.recv()
        self.game_board.update_game_board(int(move[0]), int(move[1]), 'X')
        button = self.buttons[int(move[0]) * 3 + int(move[1])]
        self.enable_buttons()
        button.config(text='X', state=tk.DISABLED)
        self.turn_label.config(text="Player 2, please make your move.")
        self.window.update()
        self.turn = True

        if self.game_board.is_winner('X'):
            self.show_message("\n\n" + f"{self.username} wins!" + "\n" + f"{self.username} is making a decision...")
            return

        if self.game_board.board_is_full():
            self.show_message("\n\n" + f"Board is full!" + "\n" + f"{self.username} is making a decision...")
            return


if __name__ == "__main__":
    server = TicTacToeServer()
    tk.mainloop()
