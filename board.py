class Board:

    def __init__(self):
        # board is a list of cells that are represented
        # by strings (" ", "O", and "X")
        # initially it is made of empty cells represented
        # by " " strings
        self.key = ('A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3')
        self.sign = " "
        self.size = 3
        self.board = list(self.sign * self.size ** 2)
        # the winner's sign O or X
        self.winner = ""

    def get_size(self):
        # optional, return the board size (an instance size)
        return self.size

    def get_winner(self):
        # return the winner's sign O or X (an instance winner)
        return self.winner

    def set(self, cell, sign):
        # mark the cell on the board with the sign X or O
        self.board[self.key.index(cell)] = sign
        # you need to convert A1, B1, …, C3 cells into index values from 1 to 9
        # you can use a tuple ("A1", "B1",...) to obtain indexes
        # this implementation is up to you

    def isempty(self, cell):
        # you need to convert A1, B1, …, C3 cells into index values from 1 to 9
        # print(self.board[self.key.index(cell)])
        return True if self.board[self.key.index(cell)] == " " else False
        # return True if the cell is empty (not marked with X or O)

    def isdone(self):
        # check horizontal

        '''board_2d = [[self.board[i], self.board[i+1], self.board[i+2]] for i in range(0, 9, 3)]'''
        for i in range(0, 7, 3):
            cur = {self.board[i], self.board[i + 1], self.board[i + 2]}
            if len(cur) == 1 and self.board[i] != " ":
                self.winner = self.board[i]
                return True
        # check vertical
        for i in range(0, 3):
            cur = {self.board[i], self.board[i+3], self.board[i+6]}
            if len(cur) == 1 and self.board[i] != " ":
                self.winner = self.board[i]
                return True
        # check diagonals
        d1, d2 = {self.board[0], self.board[4], self.board[8]}, {self.board[2], self.board[4], self.board[6]}
        for d in [d1, d2]:
            if len(d) == 1 and self.board[4] != " ":
                self.winner = self.board[4]
                return True

        if ' ' not in self.board:
            return True
        # check all game terminating conditions, if one of them is present, assign the var done to True
        # depending on conditions assign the instance var winner to O or X
        return False

    def show(self):
        sep_line = " +---+---+---+"
        # draw the board
        print("   A   B   C")
        for i in range(0, 3):
            print(sep_line)
            print(f"{i+1}| {self.board[3*i]} | {self.board[1 + 3*i]} | {self.board[2 + 3*i]} |")
        print(sep_line)
