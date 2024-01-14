import socket
import tkinter as tk
from gameboard import GameBoard

class TicTacToeClient:
    def __init__(self):
        """
        Initializes the TicTacToeClient class.
        """
        self.server_socket = None
        self.window = None
        self.buttons = []
        self.game_board = GameBoard()
        self.username = None  # Store the username here
        self.setup_window()
        self.create_buttons()
        self.turn = True

    
    def send(self, message: str):
        """
        Sends a message to the server.

        Args:
            message (str): The message to send.
        """
        self.server_socket.send(message.encode())

    def recv(self) -> str:
        """
        Receives data from the server.

        Returns:
            str: The received data.
        """
        data = self.server_socket.recv(1024).decode()
        return data

    def connect_to_server(self):
        """
        Connects to the server using the provided host and port.
        """
        try:
            host, port = self.get_host_port()
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((host, port))
            self.connect_button.config(state=tk.DISABLED)
            self.username_entry.config(state=tk.NORMAL)
            self.username_button.config(state=tk.NORMAL)
            self.username_label_display.config(text="Please enter your username.")
        except Exception:
            self.username_label_display.config(text="Could not connect. Try again.")
            self.connect_button.config(state=tk.NORMAL)


    def get_host_port(self) -> tuple:
        """
        Retrieves the host and port from the entry fields.

        Returns:
            tuple: The host and port values.
        """
        host = self.host_entry.get()
        port = self.port_entry.get()
        return host, int(port)

    def setup_window(self):
        """
        Sets up the GUI window.
        """
        self.window = tk.Tk()
        self.window.title("Taiki's Tic Tac Toe - Player 1")
        self.window.resizable(False, False)

        host_label = tk.Label(self.window, text="Host: ", font=('Arial', 12))
        host_label.grid(row=0, column=0, sticky=tk.W)
        self.host_entry = tk.Entry(self.window, font=('Arial', 10))
        self.host_entry.grid(row=0, column=1, sticky=tk.W)

        port_label = tk.Label(self.window, text="Port: ", font=('Arial', 12))
        port_label.grid(row=1, column=0, sticky=tk.W)
        self.port_entry = tk.Entry(self.window, font=('Arial', 10))
        self.port_entry.grid(row=1, column=1, sticky=tk.W)

        self.connect_button = tk.Button(self.window, text="Connect", font=('Arial', 12), command=self.connect_to_server)
        self.connect_button.grid(row=2, column=2, sticky=tk.E)
        

        label = tk.Label(self.window, text="Taiki's Tic Tac Toe", font=('Arial', 20))
        label.grid(row=2, columnspan=5, pady=10)

        self.username_label = tk.Label(self.window, text="Enter your username:", font=('Arial', 12))
        self.username_label.grid(row=3, columnspan=5, pady=5)
        self.username_entry = tk.Entry(self.window, font=('Arial', 12))
        self.username_entry.grid(row=4, columnspan=5, pady=5)
        self.username_button = tk.Button(self.window, text="Enter", font=('Arial', 12), command=self.start_game)
        self.username_button.grid(row=5, columnspan=5, pady=5)
        self.username_entry.config(state=tk.DISABLED)
        self.username_button.config(state=tk.DISABLED)

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.window, text=' ', font=('Arial', 20), width=8, height=4,
                                   command=lambda row=i, col=j: self.handle_move(row, col))
                button.grid(row=i+6, column=j)
                self.buttons.append(button)

        self.username_label_display = tk.Label(self.window, text="Please enter host and port.", font=('Arial', 14))
        self.username_label_display.grid(row=9, columnspan=3, pady=10)


        for button in self.buttons:
            button.config(text=' ', state=tk.DISABLED)

    def create_buttons(self):
        """
        Creates the Tic Tac Toe buttons.
        """
        for i in range(3):
            for j in range(3):
                button = self.buttons[i * 3 + j]
                button.config(text=' ')
                self.game_board.reset_game_board()

    def handle_move(self, row: int, col: int):
        """
        Handles a move made by the player.

        Args:
            row (int): The row index of the button.
            col (int): The column index of the button.
        """
        while self.turn == True:
            button = self.buttons[row * 3 + col]
            if button["text"] == ' ':
                if self.game_board.update_game_board(row, col, 'X'):
                    button.config(text= 'X', state=tk.DISABLED)
                    self.turn_label.config(text="Player 2 is making a move...")
                    self.window.update()
                    self.server_socket.send(f"{row}{col}".encode())
                    self.turn = False

                    if self.game_board.is_winner('X'):
                        self.show_message(f"{self.username} wins!")
                        self.game_board.num_wins()
                        self.game_board.num_games()
                        self.create_buttons()
                        self.turn = True
                        return

                    if self.game_board.board_is_full():
                        self.show_message("Board is full!")
                        self.game_board.num_ties()
                        self.game_board.num_games()
                        self.create_buttons()
                        self.turn = True
                        return
                
        while self.turn == False:
            move = self.recv()
            if len(move) == 2:
                self.game_board.update_game_board(int(move[0]), int(move[1]), 'O')
                button = self.buttons[int(move[0]) * 3 + int(move[1])]
                button.config(text='O', state=tk.DISABLED)
                self.turn_label.config(text=f"{self.username}, please make your move...")
                self.window.update()
                self.turn = True
                
                if self.game_board.is_winner('O'):
                    self.show_message("Player 2 wins!")
                    self.game_board.num_losses()
                    self.game_board.num_games()
                    self.create_buttons()
                    return

                if self.game_board.board_is_full():
                    self.show_message("Board is full!")
                    self.game_board.num_ties()
                    self.game_board.num_games()
                    self.create_buttons()
                    return

    def start_game(self):
        """
        Starts the game by sending the username to the server.
        """
        username = self.username_entry.get().strip()
        if username:
            self.username = username
            self.send(username)

            self.username = username 
            self.username_label.destroy()
            self.username_entry.destroy()
            self.username_button.destroy()
            self.username_label_display.destroy()

            username_label = tk.Label(self.window, text="Username: ", font=('Arial', 16))
            username_label.grid(row=10, column=0, sticky=tk.W)
            self.username_label = tk.Label(self.window, text=f'{self.username}', font=('Arial', 16))
            self.username_label.grid(row=10, column=1, sticky=tk.W)
        
            opponent_label = tk.Label(self.window, text="Opponent: ", font=('Arial', 16))
            opponent_label.grid(row=11, column=0, sticky=tk.W)
            self.username_label_opponent = tk.Label(self.window, text="Player 2", font=('Arial', 16))
            self.username_label_opponent.grid(row=11, column=1, sticky=tk.W)
            self.turn_label = tk.Label(self.window, text=f"{self.username}, please make your move.", font=('Arial', 14))
            self.turn_label.grid(row=9, columnspan=3, pady=10)

            #STATS
            games = tk.Label(self.window, text="Games: ", font=('Arial', 16))
            games.grid(row=12, column=0, sticky=tk.W)
            self.num_games = tk.Label(self.window, text="", font=('Arial', 16))
            self.num_games.grid(row=12, column=1, sticky=tk.W)
            wins = tk.Label(self.window, text="Wins: ", font=('Arial', 16))
            wins.grid(row=13, column=0, sticky=tk.W)
            self.num_wins = tk.Label(self.window, text="", font=('Arial', 16))
            self.num_wins.grid(row=13, column=1, sticky=tk.W)
            losses = tk.Label(self.window, text="Losses: ", font=('Arial', 16))
            losses.grid(row=14, column=0, sticky=tk.W)
            self.num_losses = tk.Label(self.window, text="", font=('Arial', 16))
            self.num_losses.grid(row=14, column=1, sticky=tk.W)
            ties = tk.Label(self.window, text="Ties: ", font=('Arial', 16))
            ties.grid(row=15, column=0, sticky=tk.W)
            self.num_ties = tk.Label(self.window, text="", font=('Arial', 16))
            self.num_ties.grid(row=15, column=1, sticky=tk.W)

            blank = tk.Label(self.window)
            blank.grid(row=16, column=1, sticky=tk.W)

            for button in self.buttons:
                button.config(text=' ', state=tk.NORMAL)
                
            self.window.update()

            
    def show_message(self, message):
        """
        Displays a message in a popup window.

        Args:
            message (str): The message to be displayed.
        """
        self.turn_label.config(text="Game Over")
        popup = tk.Toplevel()
        popup.title("Fun Times")
        popup.geometry("300x200")
        label = tk.Label(popup, text=message, font=('Arial', 14))
        label.pack(pady=20)
        
        for button in self.buttons:
            button.config(text=' ', state=tk.DISABLED)
            
        play_again_button = tk.Button(popup, text="Play Again", width=10, command=lambda: self.play_again_button_clicked(popup))
        play_again_button.pack(pady=10)
        quit_button = tk.Button(popup, text="Quit", width=10, command=lambda: self.quit_button_clicked(popup))
        quit_button.pack(pady=10)

    def play_again_button_clicked(self, popup):
        """
        Callback function for the Play Again button click.

        Args:
            popup (tk.Toplevel): The popup window object.
        """
        self.turn_label.config(text=f"Play Again! {self.username} please make a move.")
        popup.destroy()
        self.send('play_again')
        for button in self.buttons:
                button.config(state=tk.NORMAL)

    def quit_button_clicked(self, popup):
        """
        Callback function for the Quit button click.

        Args:
            popup (tk.Toplevel): The popup window object.
        """
        popup.destroy()
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        self.send(self.game_board.compute_stats(self.num_games, self.num_wins, self.num_losses, self.num_ties, self.turn_label))
        self.server_socket.close()
        self.turn_label.config(text="Fun Times")
        self.window.update()


    def run(self):
        """
        Runs the main loop of the GUI.
        """
        self.window.mainloop()

if __name__ == "__main__":
    client = TicTacToeClient()
    client.run()
