# Author: Yonatan Tal

import numpy as np
from colored import fg, bg, attr

COLORS = ['red', 'blue', 'green', 'yellow']

COLOR_LETTER_TO_NUM = {
    'r': 0,
    'b': 1,
    'g': 2,
    'y': 3,
}

UNDO_LETTER = 'u'

LEGAL_INPUT = ['r', 'b', 'g', 'y', 'u']

class Flood:
    """ 
        A class For playing the game of Flood.
    """
    __board = []
    __walked_threw_board = []
    __board_history = []
    __history_index = 0
    __moves_num = 0
    __max_moves_num = 0
    __size = 0
    __is_game_won = False

    def __init__(self, size=18, max_moves_num=21):
        """ 
            Initiating the Flood game board and number of moves.

            @size (optional) - the size of each dimention of the board (default = 18)
            @max_moves_num (optional) - the number of moves the player can make (default = 21)
        """
        self.__size = size
        self.__max_moves_num = max_moves_num
        self.__init_board()
        self.__init_board_history()

    def __init_board(self):
        """ 
            Initiating the Flood game board with random numbers (that represent colors)
        """
        self.__board = np.random.randint(len(COLORS), size=(self.__size, self.__size))

    def __init_board_history(self):
        """ 
            Initiating the Flood game history board.
        """
        self.__board_history = np.zeros((self.__max_moves_num, self.__size, self.__size)).astype(int)

    def __save_board(self):
        """ 
            Saving the current board in the history.
        """
        self.__board_history[self.__history_index] = self.__board
    
    def __restore_prev_board(self):
        """ 
            Restoring the last borad (from the history).
            In case there is no more history to go back to: does nothing.
        """
        if self.__history_index <= 0:
            # There is no more history from here :)
            return
        self.__history_index -= 1
        self.__board = self.__board_history[self.__history_index]

    def __print_board(self):
        """ 
            Printing the board game (with colors) while also checking for a win condition 
            (wether all of the tiles have the same color).
        """
        possible_win = True
        color = self.__board[0,0]
        for line in self.__board:
            for tile in line:
                if tile != color:
                    possible_win = False
                print_tile_color(tile)
            print('')
        if possible_win:
            self.__game_won()

    def play(self):
        """ 
            This function runs the flood game. Each turn the player must enter a supported letter (r/g/b/y),
            then the function spread the selected color, print the new board, and checks for a win condition.
            If the win condition is not reached within the maximum number of moves, the player loses.
            The plater can also make an 'undo' turn by entering the letter 'u'. This turn will load the last
            board from the history (if there is no history loads the current board).
        """
        self.__print_board()
        self.__save_board()
        while (self.__moves_num < self.__max_moves_num) and (not self.__is_game_won):
            self.__moves_num += 1
            print('Move ' + str(self.__moves_num) + '/' + str(self.__max_moves_num))
            input_letter = input('Please enter the next color (r/g/b/y) or u for undo:\n')
            while input_letter not in LEGAL_INPUT:
                # Ask for input till the player gives a correct one.
                input_letter = input('Unsupported letter! Please enter the next color (r/g/b/y) or u for undo:\n')
            if input_letter == UNDO_LETTER:
                self.__restore_prev_board()
            else:
                self.__spread_color(COLOR_LETTER_TO_NUM[input_letter])
                self.__history_index += 1
                self.__save_board()
            self.__print_board()
        if not self.__is_game_won: self.__game_over()

    def __game_won(self):
        """ 
            Prints a message about the win to the player and set this game as a win
        """
        print('Congratulations! You Won after ' + str(self.__moves_num) + '/' + str(self.__max_moves_num) + ' Moves!')
        self.__is_game_won = True

    def __game_over(self):
        """ 
            Prints a message about the loss to the player
        """
        print('Out of moves. Game Over!')

    def __spread_color(self, color):
        """ 
            Spreads a givven color through the board from the starting point (0,0),
            While also sets an array of the same size as the board that represents the tiles
            which was visited during this turn.

            @color - the new color to spread.
        """
        self.__walked_threw_board = np.zeros((self.__size, self.__size))
        self.__spread_color_to_neighbors((0,0), color)

    def __spread_color_to_neighbors(self, current_position, new_color):
        """ 
            Change a til's color to a new one, and spreads a givven color from a tile 
            to its neighbors under this following conditions:
                1. The color of the neighbor is the same as the old color of the tile
                2. The neighbor was not visited before during this turn.

                @current_position - the position of the tile in the game's board
                @new_color - the new color to paint the tile (and possibly its neighbors) with.
        """
        x, y = current_position
        old_color = self.__board[x,y]
        self.__board[x,y] = new_color
        self.__walked_threw_board[x,y] = True

        if (x+1 < self.__size) and (not self.__walked_threw_board[x+1, y]) and (self.__board[x+1, y] == old_color):
            self.__spread_color_to_neighbors((x+1, y), new_color)

        if (y+1 < self.__size) and (not self.__walked_threw_board[x, y+1]) and (self.__board[x, y+1] == old_color):
            self.__spread_color_to_neighbors((x, y+1), new_color)
        
        if (x > 0) and (not self.__walked_threw_board[x-1, y]) and (self.__board[x-1, y] == old_color):
            self.__spread_color_to_neighbors((x-1, y), new_color)
        
        if (y > 0) and (not self.__walked_threw_board[x, y-1]) and (self.__board[x, y-1] == old_color):
            self.__spread_color_to_neighbors((x, y-1), new_color)


def print_tile_color(tile):
    """ 
        An auxiliary function that print a tile with its color (according to the defined COLORS array).

        @tile - the tile color(number) to print.
    """
    print ('%s%s  %s' % (fg('white'), bg(COLORS[tile]), attr(0)), end='')

game = Flood(size = 18, max_moves_num=21)

game.play()
