from helpers import *
from game import *

def get_moves(loc : int, board : array) -> array:
   # Build sequentially taking into account the following:
   # - Piece Type
   # - Piece Color
   # - In Check?
   # - 50 move rule
   piece = board[loc]
   if piece == None : return []

   if abs(piece) == 1: return pawn_moves(loc, board)
   if abs(piece) == 2: return knight_moves(loc, board)
   if abs(piece) == 3: return bishop_moves(loc, board)
   if abs(piece) == 4: return rook_moves(loc, board)
   if abs(piece) == 5: return queen_moves(loc, board)
   if abs(piece) == 6: return king_moves(loc, board)

def pawn_moves(loc : int, board : list):

   # just to allow testing using alegbraic notation
   if (type(loc) == str) :
      loc = convert_loc(loc)

   result = []
   piece = board[loc]
   print(f"Piece is {piece} at location {convert_loc(loc)}")
   # white/black pieces positive/negative direction to move to tail/head of list
   direction = -1 * sgn(piece)
   print(f"Direction is {direction}")
   # List of potentially legal squares
   target_locs = [loc + direction*step for step in [9,10,11]]
   
   i = 0
   for target_loc in target_locs:
      print(f"Target number {i} is: {target_loc}, or {convert_loc(target_loc)}")
      i+=1
      print("---------------------------------")
      if valid_target_square(board[loc], board[target_loc]):
         result.append(target_loc)
   return result



