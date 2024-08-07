import tkinter as tk
import math

# Constants
HUMAN = 'O'
AI = 'X'
EMPTY = ' '

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = initialize_board()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.human_turn = True
        self.create_widgets()
    
    def create_widgets(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c] = tk.Button(self.root, text=EMPTY, font='normal 20 bold', width=5, height=2,
                                               command=lambda r=r, c=c: self.human_move(r, c))
                self.buttons[r][c].grid(row=r, column=c)
    
    def human_move(self, r, c):
        if self.board[r][c] == EMPTY and self.human_turn:
            self.board[r][c] = HUMAN
            self.buttons[r][c].config(text=HUMAN)
            self.human_turn = False
            if not self.check_game_over():
                self.root.after(500, self.ai_move)
    
    def ai_move(self):
        move = best_move(self.board)
        if move:
            r, c = move
            self.board[r][c] = AI
            self.buttons[r][c].config(text=AI)
            self.human_turn = True
            self.check_game_over()
    
    def check_game_over(self):
        if check_win(self.board, AI):
            self.show_result("AI wins!")
            return True
        if check_win(self.board, HUMAN):
            self.show_result("Human wins!")
            return True
        if check_draw(self.board):
            self.show_result("It's a draw!")
            return True
        return False
    
    def show_result(self, result):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(state=tk.DISABLED)
        result_label = tk.Label(self.root, text=result, font='normal 20 bold')
        result_label.grid(row=3, column=0, columnspan=3)
        restart_button = tk.Button(self.root, text="Restart", font='normal 20 bold', command=self.restart_game)
        restart_button.grid(row=4, column=0, columnspan=3)
    
    def restart_game(self):
        self.board = initialize_board()
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=EMPTY, state=tk.NORMAL)
        self.human_turn = True
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) > 2:
                widget.destroy()

def initialize_board():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def check_win(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

def check_draw(board):
    return all([cell != EMPTY for row in board for cell in row])

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]

def minimax(board, is_maximizing):
    if check_win(board, AI):
        return 1
    if check_win(board, HUMAN):
        return -1
    if check_draw(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for (r, c) in get_available_moves(board):
            board[r][c] = AI
            eval = minimax(board, False)
            board[r][c] = EMPTY
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for (r, c) in get_available_moves(board):
            board[r][c] = HUMAN
            eval = minimax(board, True)
            board[r][c] = EMPTY
            min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    best_value = -math.inf
    move = None
    for (r, c) in get_available_moves(board):
        board[r][c] = AI
        move_value = minimax(board, False)
        board[r][c] = EMPTY
        if move_value > best_value:
            best_value = move_value
            move = (r, c)
    return move

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
