from collections import Counter
from random import choice
from time import sleep


class Player:
    def __init__(self, name, sign):
        self.name = name  # player's name
        self.sign = sign  # player's sign O or X

    def get_sign(self):
        # return an instance sign
        return self.sign

    def get_name(self):
        # return an instance name
        return self.name

    # check if input is a valid cell
    def is_valid(self, input):
        if len(input) != 2:
            return False
        col = input[0]
        row = input[1]
        try:
            row = int(row)
            if not col.isalpha() or not 1 <= row <= 3:
                return False
        except:
            return False

        return True

    # prompt the user to enter a cell
    def choose(self, board):
        # prompt the user to choose a cell
        cell = input(f"{self.name}, {self.sign}: Enter a cell [A-C][1-3]: \n").upper()
        try:
            # check if the input is valid
            if self.is_valid(cell):
                # check if board is empty
                if board.isempty(cell):
                    board.set(cell, self.sign)
                else:
                    raise Exception
            else:
                raise Exception
        except:
            # if the user enters a valid string and the cell on the board is empty, update the board
            print("You did not choose correctly.")
            self.choose(board)
        # otherwise print a message that the input is wrong and rewrite the prompt
        # use the methods board.isempty(cell), and board.set(cell, sign)


class AI(Player):
    def __init__(self, name, sign, board):
        super().__init__(name, sign)
        self.board = board
        self.available_spaces = []

    # randomly choose place to put sign
    def choose(self, board):
        # find all available spaces on the board
        self.available_spaces = [space for space, num in zip(board.key, board.board) if num == " "]
        # choose a random space
        cell = choice(self.available_spaces)
        # use sleep to make the game easier to follow
        sleep(1)
        print(cell)
        sleep(1)
        board.set(cell, self.sign)


class SmartAI(AI):
    def __init__(self, name, sign, board):
        super().__init__(name, sign, board)
        self.board = board
        self.available_spaces = []
        if self.sign == "X":
            self.opponent = "O"
        else:
            self.opponent = "X"

    def can_win_or_block(self):
        # check if AI or the player can win
        # return the cell where AI can win or block
        # check horizontal
        for i in range(0, 7, 3):
            l = [self.board.board[i], self.board.board[i + 1], self.board.board[i + 2]]
            cur = Counter(l)
            if cur['X'] == 2 and cur[' '] == 1 or cur['O'] == 2 and cur[' '] == 1:
                return self.board.key[l.index(' ') + i]
        # check vertical
        for i in range(0, 3):
            l = [self.board.board[i], self.board.board[i + 3], self.board.board[i + 6]]
            cur = Counter(l)
            if cur['X'] == 2 and cur[' '] == 1 or cur['O'] == 2 and cur[' '] == 1:
                return self.board.key[i + l.index(' ') * 3]
        # check diagonals
        d1, d2 = Counter([self.board.board[0], self.board.board[4], self.board.board[8]]), Counter([self.board.board[2], self.board.board[4], self.board.board[6]])
        if d1['X'] == 2 and d1[' '] == 1 or d1['O'] == 2 and d1[' '] == 1:
            s = (self.board.key[self.board.board[0:9:4].index(' ')])
            if s == 0:
                return self.board.key[0]
            return self.board.key[4] if s == 1 else self.board.key[8]
        if d2['X'] == 2 and d2[' '] == 1 or d2['O'] == 2 and d2[' '] == 1:
            s = (self.board.key[self.board.board[0:9:4].index(' ')])
            if s == 0:
                return self.board.key[2]
            return self.board.key[4] if s == 1 else self.board.key[6]
        return ''

    def fork(self):
        # check if AI can fork
        # return the cell where AI can fork
        move = ''
        for cell in self.available_spaces:
            board = self.board
            board.set(cell, self.sign)
            # check if AI can win
            if self.can_win_or_block() != '':
                board.set(cell, ' ')
                move = cell
            board.set(cell, ' ')
        return move

    def other_fork(self):
        # check if the other player can fork
        # return the cell where the player can fork
        move = ''
        for cell in self.available_spaces:
            board = self.board
            board.set(cell, self.opponent)
            # check if the player can win
            if self.can_win_or_block() != '':
                board.set(cell, ' ')
                move = cell
            board.set(cell, ' ')
        return move

    def center_available(self):
        # check if the center is available
        # return True if the center is available
        return self.board.board[4] == ' '

    def opposite_corner(self):
        # check if opponent is in a corner
        # if so, return the opposite corner
        if self.board.board[0] == self.opponent and self.board.board[8] == ' ':
            return self.board.key[8]
        elif self.board.board[2] == self.opponent and self.board.board[6] == ' ':
            return self.board.key[6]
        elif self.board.board[6] == self.opponent and self.board.board[2] == ' ':
            return self.board.key[2]
        elif self.board.board[8] == self.opponent and self.board.board[0] == ' ':
            return self.board.key[0]
        return ''

    def empty_corner(self):
        # check if there is an empty corner
        # return the empty corner
        for i in [0, 2, 6, 8]:
            if self.board.board[i] == ' ':
                return self.board.key[i]
        return ''

    def empty_side(self):
        # check if there is an empty side
        # return the empty side
        for i in [1, 3, 5, 7]:
            if self.board.board[i] == ' ':
                return self.board.key[i]
        return ''

    def choose_algorithm(self, board):
        # get all empty spaces
        self.available_spaces = [space for space, num in zip(board.key, board.board) if num == " "]
        can_move = self.can_win_or_block()
        if can_move != '':
            print(can_move)
            return can_move
        can_move = self.fork()
        if can_move != '':
            print(can_move)
            return can_move
        can_move = self.other_fork()
        if can_move != '':
            print(can_move)
            return can_move
        can_move = 'B2'
        if self.center_available():
            print(can_move)
            return can_move
        can_move = self.opposite_corner()
        if can_move != '':
            print(can_move)
            return can_move
        can_move = self.empty_corner()
        if can_move != '':
            print(can_move)
            return can_move
        can_move = self.empty_side()
        print(can_move)
        return can_move

    def choose(self, board):
        print(f"\n{self.name}, {self.sign}: Enter a cell [A-C][1-3]: ")
        board.set(self.choose_algorithm(board), self.sign)


class MiniMax(AI):
    def __init__(self, name, sign, board, other):
        super().__init__(name, sign, board)
        self.other = other

    # choose place to place the sign
    def choose(self, board):
        # establish base low score and initialize best move
        best_score = -1000
        best_move = 0

        print(f"\n{self.name}, {self.sign}: Enter a cell [A-C][1-3]: ")
        # start the minimax algorithm
        for space in self.board.key:
            if self.board.isempty(space):
                self.board.set(space, self.sign)
                score = self.minimax(self.board, 0, False)
                self.board.set(space, ' ')
                self.board.winner = ""
                if score > best_score:
                    best_score = score
                    best_move = space

        # print the best move and continue the game
        print(best_move)
        self.board.set(best_move, self.sign)
        return

    # minimax recursive algorithm
    def minimax(self, board, depth, is_maximizing):
        # check the base conditions
        if self.board.isdone():
            # self is a winner
            if self.board.get_winner() == self.sign:
                return 1
            # check for draw
            elif self.board.get_winner() == self.other.sign:
                return -1
            # player is winner
            else:
                return 0
        # make a move (choose a cell) recursively
        # plays game as the bot
        if is_maximizing:
            best_score = -800

            for space in self.board.key:
                if self.board.isempty(space):
                    self.board.set(space, self.sign)
                    score = self.minimax(self.board, depth + 1, False)
                    self.board.set(space, ' ')
                    self.board.winner = ""
                    if score > best_score:
                        best_score = score

            return best_score

        # plays game as the player
        else:
            best_score = 800

            for space in self.board.key:
                if self.board.isempty(space):
                    self.board.set(space, self.other.sign)
                    score = self.minimax(self.board, depth + 1, True)
                    self.board.set(space, ' ')
                    self.board.winner = ""
                    if score < best_score:
                        best_score = score

            return best_score
