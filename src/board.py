import board_helpers
import helpers
import moves

class Board:
   """
   Board object is a container game data and methods to manipulate that data.
   """
   def __init__( self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
      (self.fen,
       self.active_color,
       self.castling,
       self.en_passant,
       self.half_move,
       self.full_move) = fen.split()
      
      self.array = board_helpers.make_board(self.fen)
      self.half_move = int(self.half_move)
      self.full_move = int(self.full_move)

   def __str__(self):
      print("—"*72)
      board_helpers.print_board_array(self)
      print("—"*72)
      print(
         "Active color:             " + self.active_color,
         "Current Move number:      " + str(self.full_move),
         "Castling:                 " + self.castling,
         "En passant:               " + self.en_passant,
         "FEN:                      " + self.fen,
         sep="\n"
      )
      print("—"*72, end = '')
      return ""

   def push(self, lan : str): #lan here is long algebraic notation
      start_coor, end_coor = helpers.convert_lan(lan)
      
      #check legality
      legal_moves = moves.get_moves(start_coor,self)
      
      # If legal, make move and update data
      if end_coor in legal_moves:
         self.array[end_coor] = self.array[start_coor]
         self.array[start_coor] = 0

         # Update active_color and move count
         if self.active_color == 'b': 
            self.active_color = 'w'
            self.full_move += 1
            self.half_move += 1
         else: self.active_color = 'b'

      return self
