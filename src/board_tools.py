import move
import parse_tools as pt
import board_tools as bt

def print_board_array(self):
   # To print the board in a standard format, we must go in the following order:
   # 81...88/.../11...18
   for rank in reversed(range(12)):
      for file in range(12):
         square = rank*12 + file # for when I mess up coorddinates, inevitably
         # print empty squares as '_'
         if self.array[square] == 0:
            print(" . ", end ='')
         # else, print non-None values
         elif self.array[square] is not None: 
            print(f" {piece_rep(self.array[square])} ", end = '')
         # Newline after 8 files, exlcuding boundary squares
         if file == 11 and (not (rank in [0,1,10,11])):
            print("\n", end = '')
   return ""

def make_board(fen : str):
   """
   Accepts a FEN string and returns a 12x12 1D array board
   representation with border padding.
   """
   result = [None] * 26
   rows = fen.split('/')
   rows = reversed(rows)
   for row in rows:
      for char in row:
         if char.isdigit():                           # add empty squares
            result.extend([0]*int(char))
         else:                                        # add pieces
            result.append(piece_rep(char))
      result.extend([None]*4)
   result = result + [None] * 22    # add 0 and 9th row padding
   return result

def piece_rep(piece):
   """ 
   Converts between character and integer represenation for printing purposes
   and FEN construction 
   """
   pieces = ['P','N','B','R','Q','K']
   if(type(piece) == str):
      if piece == piece.upper():
         return ( pieces.index(piece) + 1 )
      else:
         return ( -1 ) * ( pieces.index(piece.upper()) + 1 )
   elif(type(piece) == int):
      if piece < 0 :
         return pieces[(-1)*piece - 1].lower()
      else:
         return pieces[piece - 1]

def find_kings(board):
   """
   Returns list of King locations. Run during board initialisation.
   """
   result = [None,None]
   for square in range(len(board.array)):
      if board.array[square] == 6:
         result[0] = square
      if board.array[square] == -6:
         result[1] = square

   return result 

def update_meta(board: Board, from_square : int, to_square : int):
   
   update_castling_rights(board, from_square, to_square)
   update_en_passant(board, from_square, to_square)
   update_turn_fields(board) # move number and active_color

   # Update board by replacing elements
   board.array[to_square] = from_piece
   board.array[from_square] = 0

def update_castling_rights(board : Board, from_square: int, to_square : int) -> bool:

   from_piece = board.array[from_square]
   if from_piece == 6:
      board.white_king = to_square
      board.castling = board.castling.replace('K','')
      board.castling = board.castling.replace('Q','')
      return True

   elif from_piece ==  -6:
      board.black_king = to_square
      board.castling = board.castling.replace('k','')
      board.castling = board.castling.replace('q','')
      return True

   else: 
      return False

def update_en_passant(board: Board, from_square : int, to_square : int) -> bool:
   
   direction = board.array[from_square] // abs(board.array[from_square])

   if move.is_enpassantable(board, from_square, to_square):
      board.en_passant = pt.convert_loc(to_square - direction*move.NORTH)
   else:
      board.en_passant = '-'

   return True

def update_turn_fields(board : Board):
   self.active_color = -1 * self.active_color
   self.half_move += 1
   if self.active_color == 1: 
      self.full_move += 1


