from helpers import *
from game import *

# Not the best, but Black is not affected becuase color determines
# orientation and therefore sign of the travel step.
north = 12
south = -12
east = 1
west = -1
north_east = 13
north_west = 11
south_east = -11
south_east = -13


def get_moves(loc : int, board : array) -> array:
   # Build sequentially taking into account the following:
   # - Piece Type
   # - Piece Color
   # - In Check?
   # - 50 move rule
   if (type(loc) == str) :
      loc = convert_loc(loc)
   piece = board[loc]
   if piece == None : return []

   if abs(piece) == 1: return pawn_moves(loc, board)
   if abs(piece) == 2: return knight_moves(loc, board)
   if abs(piece) == 3: return bishop_moves(loc, board)
   if abs(piece) == 4: return rook_moves(loc, board)
   if abs(piece) == 5: return queen_moves(loc, board)
   if abs(piece) == 6: return king_moves(loc, board)

def pawn_moves(start_idx : int, board : list):
   #TODO: Add en passant

   # just to allow testing using alegbraic notation
   if (type(start_idx) == str) :
      start_idx = convert_loc(start_idx)

   result = []
   piece = board[start_idx]
   # FLAGS:

   # White/black pieces move in positve/negative direction up the board
   direction = sgn(piece)  
   # On starting row?
   on_starting_row = start_idx // 12 in [3,8]

   for step in [north_west, north, north_east, north*2]:

      target_idx = start_idx + direction*step
      end_value = board[target_idx]
   
      if (end_value is None):                      # Do not move off the board
         continue
      elif sgn(piece) == sgn(end_value):           # Do not capture friendly pieces
         continue
      # Pawns can only capture diagonally
      elif (sgn(piece)*sgn(end_value) == -1) and step in [north_west, north_east]:
         result.append(target_idx)
      # Move forward an empty square
      elif end_value == 0 and step == north:
         result.append(target_idx)
      # Allow two step if on starting rank and nothing blocking intermediate square
      elif on_starting_row and step == north*2 and end_value == 0 and board[target_idx + direction*south] == 0:
         result.append(target_idx)

   return result


def knight_moves(start_idx : int, board : list):
   # just to allow testing using alegbraic notation
   if (type(start_idx) == str) :
      start_idx = convert_loc(start_idx)

   result = []
   piece = board[start_idx]
   # white/black pieces positive/negative direction to move to tail/head of list
   direction = sgn(piece)

   for step in [10,23,25,14,-10,-23,-25,-14]:
      end_idx = start_idx + direction*step
      start_value = board[start_idx]
      end_value = board[end_idx]
      direction = sgn(start_value)
   
      if (end_value is None):                         # Do not move off the board
         continue
      elif sgn(start_value) == sgn(end_value):        # Do not capture friendly pieces
         continue
      elif (sgn(start_value)*sgn(end_value) <= 0):    # Capture opposing pieces
         result.append(end_idx)                                  # or jump to empty square
   return result

def valid_diag_move(board : list, start_idx : int, end_idx : int) -> bool :
   """
      Returns a boolean depending on whether a given target square is valid for a
      diagonal moving piece to move to or to capture.

      args: board : list, start_idx : int, end_idx : int
   """
   start_value = board[start_idx]
   end_value = board[end_idx]
   direction = sgn(start_value)

   if (end_value is None):                         # Do not move off the board.
      return False
   elif sgn(start_value) == sgn(end_value):        # Do not capture friendly pieces.
      return False
   elif (sgn(start_value)*sgn(end_value) <= 0):    # Capture opposing pieces,
      return True                                  # or jump to empty square.


