import parse_tools as pt
import board
# Not the best, but Black is not affected becuase color determines
# orientation and therefore sign of the travel step.

NORTH = 12
SOUTH = -12
EAST = 1
WEST = -1
NORTH_EAST = 13
NORTH_WEST = 11
SOUTH_EAST = -11
SOUTH_WEST = -13

piece_steps = {
   1 : [NORTH, NORTH_WEST, NORTH_EAST],
   2 : [10,23,25,14,-10,-23,-25,-14],
   3 : [NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST],
   4 : [NORTH, SOUTH, EAST, WEST],
   5 : [NORTH,SOUTH, EAST, WEST, NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST],
   6 : [NORTH,SOUTH, EAST, WEST, NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST]
}

class Move:
   def __init__(self, from_square : int, to_square : int, from_piece : int, to_piece : int, en_passant : str, en_passanted : int = 0):
      self.from_square = from_square
      self.to_square = to_square
      self.from_piece = from_piece
      self.to_piece = to_piece
      self.en_passant = en_passant # State before move 
      self.en_passanted = en_passanted

   def __str__(self):
      print(f"From: {pt.convert_loc(self.from_square)}")
      print(f"Piece: {self.from_piece}")
      print(f"To:   {pt.convert_loc(self.to_square)}")
      print(f"Piece: {self.to_piece}")
      print(f"en_passant: {self.en_passant}")
      return ""
# High-level callers, for lack of a better term
def get_all_moves(board : Board):

   # Retrieve active_color
   active_color = board.active_color
   
   # Result 
   result = {}

   # Move through all squares
   for square_idx in range(len(board.array)):
      temp_moves = get_legal_moves(board, square_idx, True)
      if len(temp_moves) > 0:
         result[pt.convert_loc(square_idx)] = temp_moves
   return result 
   
def get_legal_moves(board : Board, start_idx : int, san_flag = False) -> list:

   # If not turn to move, return empty array, else find legal moves
   if not(board.array[start_idx] is None) and not(turn_to_move(board.array[start_idx], board.active_color)): 
      return []
   # Find all moves first, then filter ones which puts King in check
   all_moves = get_moves(board, start_idx, False)
   active_color = board.array[start_idx]
   result = []
   for move in all_moves:
      board.push_idx(start_idx, move)
      if not(in_check(board,active_color)):
         if san_flag:
            result.append(pt.convert_loc(move))
         else:
            result.append(move)
      board.pop()
   return result

def get_moves(board : Board, loc : int, san_flag = False) -> list:
   # Build sequentially taking into account the following:
   # - Piece Type
   # - Piece Color
   # - In Check?
   # - 50 move rule
   if (type(loc) == str) :
      loc = convert_loc(loc)
   piece = board.array[loc]

   if piece == None or piece == 0 or board.active_color*piece < 0 : return []

   moves_fcts = [pawn_moves, knight_moves, bishop_moves, rook_moves, queen_moves, king_moves]
   if san_flag:
      return list(map(pt.convert_loc, moves_fcts[abs(piece) - 1](board, loc)))
   else:
      return moves_fcts[abs(piece) - 1](board, loc)

# Callers, for lack of a better term
def pawn_moves(board : Board, start_idx : int) -> list:

   # just to allow testing using alegbraic notation
   if (type(start_idx) == str) :
      start_idx = convert_loc(start_idx)

   return pawn_walks(board, start_idx) + pawn_captures(board, start_idx)

def bishop_moves(board : Board, start_idx : int) -> list:
   bishop_steps = [NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST]
   return slide_moves(board, start_idx, bishop_steps)

def rook_moves(board : Board, start_idx : int) -> list:
   rook_steps = [NORTH, SOUTH, EAST, WEST]
   return slide_moves(board, start_idx, rook_steps)

def queen_moves(board : Board, start_idx : int) -> list:
   queen_steps = [NORTH, SOUTH, EAST, WEST, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST]
   return slide_moves(board, start_idx, queen_steps)

def king_moves(board : Board, start_idx : int) -> list:
   return king_walks(board, start_idx) + king_castles(board, start_idx)
# Calculators, for lack of a better term
def pawn_walks(board : Board, start_idx : int) -> list:
   result = []
   piece = board.array[start_idx]

   # White/black pieces move in positve/negative direction up the board
   direction = pt.sgn(piece)  
   # On starting row?
   on_starting_row = start_idx // 12 in [3,8]
   
   for step in [NORTH, NORTH*2]:

      target_idx = start_idx + direction*step
      end_value = board.array[target_idx]

      # Don't march off the board or when blocked by any piece
      if (end_value is None or end_value != 0):
         break
      # Move forward an empty square
      elif step == NORTH:
         result.append(target_idx)
      # Allow two step if on starting rank
      ## Note that first condition guarantees no blocking piece
      elif on_starting_row and step == NORTH*2 and end_value == 0:
         result.append(target_idx)

   return result

def pawn_captures(board : Board, start_idx : int) -> list:
   
   result = []
   piece = board.array[start_idx]

   # White/black pieces move in positve/negative direction up the board
   direction = pt.sgn(piece)

   for step in [NORTH_WEST, NORTH_EAST]:
      target_idx = start_idx + direction*step
      end_value = board.array[target_idx]
   
      if ( end_value is not None and piece*end_value < 0 ) :
         result.append(target_idx)
      
      # en passant
      elif pt.convert_loc(target_idx) == board.en_passant:
         result.append(target_idx)
      
   return result

def knight_moves(board : Board, start_idx : int) -> list:
   # just to allow testing using alegbraic notation
   if (type(start_idx) == str) :
      start_idx = convert_loc(start_idx)

   result = []
   piece = board.array[start_idx]
   # white/black pieces positive/negative direction to move to tail/head of list
   direction = pt.sgn(piece)

   for step in [10,23,25,14,-10,-23,-25,-14]:
      end_idx = start_idx + direction*step
      start_value = board.array[start_idx]
      end_value = board.array[end_idx]
      direction = pt.sgn(start_value)

      if (end_value is None):                         # Do not move off the board
         continue
      elif pt.sgn(start_value) == pt.sgn(end_value):        # Do not capture friendly pieces
         continue
      elif (pt.sgn(start_value)*pt.sgn(end_value) <= 0):    # Capture opposing pieces
         result.append(end_idx)                                  # or jump to empty square
   return result

def king_walks(board : Board, start_idx : int) -> bool:
   result = []
   piece = board.array[start_idx]
   # White/black pieces move in positve/negative direction up the board
   direction = pt.sgn(piece)  

   for step in [NORTH, SOUTH, EAST, WEST, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST]:
      target_idx = start_idx + direction*step
      end_value = board.array[target_idx]
   
      if (end_value is None):                      # Do not move off the board
         continue
      elif pt.sgn(piece) == pt.sgn(end_value):           # Do not capture friendly pieces
         continue
      elif (piece*end_value < 0):      # Capture enemy pieces
         result.append(target_idx)
      elif end_value == 0:                         # Move to an empty square
         result.append(target_idx)
   return result

def king_castles(board : Board, start_idx : int) -> list:
   # Conditions for castling:
   # 1. Castling path cannot be blocked by any piece on any side
   # 2. King cannot be in check at any point along castling path
   # 3. Must be both King and Rook's first move. 
   
   result = []
   piece = board.array[start_idx]
   direction_steps = get_castling_steps(board, start_idx)

   for direction in direction_steps:
      for step in direction:
         target_idx = start_idx + step
         end_value = board.array[target_idx]
   
         # Cannot be blocked by any piece whatsoever:
         if end_value != 0:
            break
         # Cannot be in check at any point along path:
         elif board.push_idx(start_idx, target_idx) and in_check(board, piece):
            board.pop()
            break
         # Pop from previous condition and if at final square append it.
         elif board.pop() and abs(step) == EAST*2:
            result.append(target_idx)
   
   return result

def slide_moves(board : Board, start_idx : int, steps : list) -> list:
   result = []
   piece = board.array[start_idx]
   direction = pt.sgn(piece)

   for step in steps:
         curr_idx = start_idx

         while True:
            curr_idx = curr_idx + direction*step
            end_value = board.array[curr_idx]
   
            # Do not move off the board
            if (end_value is None): 
               break
            # Do not capture friendly pieces
            elif pt.sgn(piece) == pt.sgn(end_value): 
               break
            # Capture oppossing pieces and then stop
            elif (piece*end_value < 0 ):
            # Check if this casues check:
               result.append(curr_idx)
               break
            # Move to empty square and keep searching
            elif (end_value == 0):
               result.append(curr_idx)
   return result

# In Check?
def in_check(board : Board, active_color : int = 0) -> bool:
   # We check if a King is in check by verifying if a King can 'see' any opposing piece
   # with the vision of an amazon piece (queen + knight).
  
   # Pick right king location based on active_color
   if active_color > 0:
      king_loc = board.white_king
   elif active_color < 0:
      king_loc = board.black_king
   else:
      return in_check(board,1) or in_check(board, -1)

   
   if king_loc is None:
      return False

   # Get list of squares seen by King with each piece type's vision
   ## Room to optimise here, we double check some squares with king_squares
   pawn_squares = pawn_captures(board, king_loc)
   knight_squares = knight_moves(board, king_loc)
   bishop_squares = bishop_moves(board, king_loc)
   rook_squares = rook_moves(board, king_loc)
   king_squares = king_walks(board, king_loc)
   # Iterate through list of squares seen by King and check if they contain opposing 
   # pieces with matching vision.
   for piece_types, piece_squares in zip([[1],[2],[3,5],[4,5],[6]],[pawn_squares, knight_squares,bishop_squares,rook_squares,king_squares]):
      for square in piece_squares:
         if (abs(board.array[square]) in piece_types) and board.array[square]*active_color < 0 :
            
            return True
   
   return False

# Helpers
def turn_to_move(piece : int, active_color : int ) -> bool :
   return active_color * piece > 0

def is_enpassantable(board : Board, start_idx : int, end_idx : int):
   # Check is done before pieces are moved on the board
   result = False
   piece = board.array[start_idx]
   EAST_piece = board.array[end_idx + EAST]
   WEST_piece = board.array[end_idx + WEST]
   # Double jump
   if abs(start_idx - end_idx) == NORTH * 2 and abs(piece) == 1:
      # Not None and has adjacent opposing pawns
      if EAST_piece and EAST_piece * piece == -1:
         result = True
      elif WEST_piece and WEST_piece * piece == -1:
         result = True
   return result

def get_castling_steps(board : Board, start_idx : int) -> list:
   result = []
   piece = board.array[start_idx]

   if piece < 0:
      if 'k' in board.castling:
         result.append([EAST, EAST*2])
      if 'q' in board.castling:
         result.append([WEST, WEST*2])
   elif piece > 0 :
      if 'K' in board.castling:
         result.append([EAST, EAST*2])
      if 'Q' in board.castling:
         result.append([WEST, WEST*2])

   return result
