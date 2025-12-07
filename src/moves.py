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

def pawn_moves(loc, board):
   piece = board[loc]

   #TODO
   

