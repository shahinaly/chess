from board import *

class Game:
   """ A game object is a container for game-level information """

   def __init__( self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
      (self.board_fen,
       self.active_color,
       self.castling,
       self.en_passant,
       self.half_move,
       self.full_move) = fen.split()
      
      self.board = Board(self.board_fen)
      self.half_move = int(self.half_move)
      self.full_move = int(self.full_move)

   def __str__(self):
      print("—"*64)
      print(self.board, end = '')
      print("—"*64)
      print(
         "Active color:    " + self.active_color,
         "Move number:     " + str(self.full_move),
         "Castling:        " + self.castling,
         "En passant:      " + self.en_passant,
         "FEN:             " + self.board.fen,
         sep="\n"
      )
      print("—"*64, end = '')
      return ""
