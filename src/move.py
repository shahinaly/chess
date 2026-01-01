import parse_tools as pt
import board
# Not the best, but Black is not affected becuase color determines
# orientation and therefore sign of the travel step.
north = 12
south = -12
east = 1
west = -1
north_east = 13
north_west = 11
south_east = -11
south_west = -13

class Move:
   def __init__(self, from_square : int, to_square : int, from_piece : int, to_piece : int):
      self.from_square = from_square
      self.to_square = to_square
      self.from_piece = from_piece
      self.to_piece = to_piece

def get_moves(loc : int, board : array) -> array:
   # Build sequentially taking into account the following:
   # - Piece Type
   # - Piece Color
   # - In Check?
   # - 50 move rule
   if (type(loc) == str) :
      loc = convert_loc(loc)
   piece = board.array[loc]
   if piece == None or piece == 0 : return []

   if abs(piece) == 1: return pawn_moves(loc, board)
   if abs(piece) == 2: return knight_moves(loc, board)
   if abs(piece) == 3: return bishop_moves(loc, board)
   if abs(piece) == 4: return rook_moves(loc, board)
   if abs(piece) == 5: return queen_moves(loc, board)
   if abs(piece) == 6: return king_moves(loc, board)

def pawn_moves(start_idx : int, board : Board) -> list:
   #TODO: Add en passant

   # just to allow testing using alegbraic notation
   if (type(start_idx) == str) :
      start_idx = convert_loc(start_idx)

   return pawn_walks(start_idx, board) + pawn_captures(start_idx, board)

def pawn_walks(start_idx : int, board : Board) -> list:
   result = []
   piece = board.array[start_idx]

   # White/black pieces move in positve/negative direction up the board
   direction = pt.sgn(piece)  
   # On starting row?
   on_starting_row = start_idx // 12 in [3,8]
   
   for step in [north, north*2]:

      target_idx = start_idx + direction*step
      end_value = board.array[target_idx]

      # Don't march off the board or when blocked by any piece
      if (end_value is None or end_value is not 0):
         break
      # Move forward an empty square
      elif step == north:
         result.append(target_idx)
      # Allow two step if on starting rank
      ## Note that first condition guarantees no blocking piece
      elif on_starting_row and step == north*2 and end_value == 0:
         result.append(target_idx)

   return result

def pawn_captures(start_idx : int, board : Board) -> list:
   
   result = []
   piece = board.array[start_idx]

   # White/black pieces move in positve/negative direction up the board
   direction = pt.sgn(piece)

   for step in [north_west, north_east]:
      target_idx = start_idx + direction*step
      end_value = board.array[target_idx]
   
      if ( end_value is not None and piece*end_value < 0 ) :
         result.append(target_idx)

   return result

def knight_moves(start_idx : int, board : Board) -> list:
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

def bishop_moves(start_idx : int, board : Board) -> bool:
   bishop_steps = [north_west, north_east, south_west, south_east]
   return slide_moves(start_idx, board, bishop_steps)

def rook_moves(start_idx : int, board : Board) -> bool:
   rook_steps = [north, south, east, west]
   return slide_moves(start_idx, board, rook_steps)

def queen_moves(start_idx : int, board : Board) -> bool:
   queen_steps = [north, south, east, west, north_west, north_east, south_west, south_east]
   return slide_moves(start_idx, board, queen_steps)

def king_moves(start_idx : int, board : Board ) -> bool:
   result = []
   piece = board.array[start_idx]
   # White/black pieces move in positve/negative direction up the board
   direction = pt.sgn(piece)  

   for step in [north, south, east, west, north_west, north_east, south_west, south_east]:
      target_idx = start_idx + direction*step
      end_value = board.array[target_idx]
   
      if (end_value is None):                      # Do not move off the board
         continue
      elif pt.sgn(piece) == pt.sgn(end_value):           # Do not capture friendly pieces
         continue
      elif (pt.sgn(piece)*pt.sgn(end_value) == -1):      # Capture enemy pieces
         result.append(target_idx)
      elif end_value == 0:                         # Move to an empty square
         result.append(target_idx)
   return result

def slide_moves(start_idx : int, board : Board, steps : list) -> list:
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
            elif (pt.sgn(piece)*pt.sgn(end_value) == -1 ):
               result.append(curr_idx)
               break
            # Move to empty square and keep searching
            elif (end_value == 0):
               result.append(curr_idx)
   return result

def in_check(board : Board, king_location : int):
   # We check if a King is in check by verifying if a King can 'see' any opposing piece
   # with the vision of an amazon piece (queen + knight).
   
   king_piece = board.array[king_location]

   # Get list of squares seen by King with each piece type's vision
   ## Room to optimise here, we double check some squares with king_squares
   pawn_squares = pawn_captures(king_location,board)
   knight_squares = knight_moves(king_location, board)
   bishop_squares = bishop_moves(king_location, board)
   rook_squares = rook_moves(king_location, board)
   king_squares = king_moves(king_location,board)

   # Iterate through list of squares seen by King and check if they contain opposing 
   # pieces with matching vision.
   for piece_types, piece_squares in zip([[1],[2],[3,5],[4,5],[6]],[pawn_squares, knight_squares,bishop_squares,rook_squares,king_squares]):
      for square in piece_squares:
         if (abs(board.array[square]) in piece_types) and board.array[square]*king_piece < 0 :
            return True
   
   return False

