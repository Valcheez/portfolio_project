# Author: Aldo Valdez
# Github username: Valcheez
# Date: 6/9/24
# Description: Portfolio Project

class Piece:
    """Initializes a piece color and type"""
    def __init__(self, color, piece_type):
        self._color = color
        self._type = piece_type
        self._first_move = False

    def get_color(self):
        """Returns the color of the piece"""
        return self._color

    def get_type(self):
        """Returns the type of piece"""
        return self._type

    def valid_move(self, start, end, board):
        """checks if a move is valid for a piece"""
        if self._type == 'King':
            return False  # Kings cannot capture
        return True

class ChessVar:
    """“Initializes the board, manages the game, processes moves, and updates the board."""
    def __init__(self):
        self._board = self.chess_board()
        self._turn = 'white'
        self._game_state = 'UNFINISHED'

    def chess_board(self):
        """Initializes the board and determines the first turn"""
        board = {}
        columns = 'abcdefgh'
        rows = '12345678'

        for col in columns:
            for row in rows:
                board[col + row] = None  # Sets the position as initially empty
        for col in columns: # Place pawns
            board[col + '2'] = Piece('white', 'Pawn')
            board[col + '7'] = Piece('black', 'Pawn')
        placement = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']   # Place other pieces
        for i, piece_type in enumerate(placement):  # Places the pieces for white and black
            board[columns[i] + '1'] = Piece('white', piece_type)
            board[columns[i] + '8'] = Piece('black', piece_type)

        return board

    def get_game_state(self):
        """Returns current game state"""
        return self._game_state

    def make_move(self, start, end):
        """Ensures the game's rules and conditions are met"""
        if self._game_state != 'UNFINISHED':
            return False
        piece = self._board.get(start)
        if piece is None or piece.get_color() != self._turn:
            return False
        if not piece.valid_move(start, end, self._board):
            return False

        self.execute_move(start, end)
        self.check_explosions(end)
        self.switch_turns()
        self.update_game_state()
        return True

    def execute_move(self, start, end):
        """Moves a piece from the start to the end position"""
        self._board[end] = self._board[start]
        self._board[start] = None

    def check_explosions(self, position):
        """Checks for explosions around a position if a piece is taken"""
        capture_piece = self._board[position]
        if capture_piece:
            affected_positions = self.get_surrounding_positions(position)
            for pos in affected_positions:
                self._board[pos] = None
            self._board[position] = None

    def get_surrounding_positions(self, position):
        """Returns a list of positions surrounding a given position"""
        col, row = position
        surrounding_positions = []
        columns = 'abcdefgh'
        rows = '12345678'
        col_index = columns.index(col) # the index of the current column
        row_index = rows.index(row)     # the index of the current row

        for d_col in [-1, 0, 1]:    # offsets for the columns
            for d_row in [-1, 0, 1]:    # offsets for the rows
                if d_col == 0 and d_row == 0:   # skips the current iteration
                    continue
                new_col_index = col_index + d_col
                new_row_index = row_index + d_row
                if 0 <= new_col_index < 8 and 0 <= new_row_index < 8: # if valid, converts indexes back to col and row char
                    new_col = columns[new_col_index]
                    new_row = rows[new_row_index]
                    surrounding_positions.append(new_col + new_row)
        return surrounding_positions

    def switch_turns(self):
        """Switches players"""
        self._turn = 'black' if self._turn == 'white' else 'white'

        def update_game_state(self):
        """Checks if the game has been won"""
        king_positions = {pos: piece for pos, piece in self._board.items() if piece and piece.get_type() == 'King'}
        white_king_alive = any(piece.get_color() == 'white' for piece in king_positions.values())
        black_king_alive = any(piece.get_color() == 'black' for piece in king_positions.values())

        if not white_king_alive:
            self._game_state = 'BLACK_WON'
        elif not black_king_alive:
            self._game_state = 'WHITE_WON'

    def print_board(self):
        """Prints the board in a readable format"""
        columns = 'abcdefgh'
        rows = '87654321'
        print('  a  b  c  d  e  f  g  h')
        for row in rows:
            row_display = row + ' '
            for col in columns:
                piece = self._board[col + row]
                if piece:
                    row_display += piece.get_type()[0].upper() if piece.get_color() == 'white' else piece.get_type()[0].lower()
                else:
                    row_display += '.'
                row_display += '  '
            print(row_display)
        print()
