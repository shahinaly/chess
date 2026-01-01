import board_tools as bt
import parse_tools as pt
import move

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
      
      self.array = bt.make_board(self.fen)
      self.half_move = int(self.half_move)
      self.full_move = int(self.full_move)
      self.history = []

   def __str__(self):
      print("—"*72)
      bt.print_board_array(self)
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

   def push_lan(self, lan : str) -> Board: #lan here is long algebraic notation
      from_square, to_square = pt.convert_lan(lan)
      from_piece = self.array[from_square]
      to_piece = self.array[to_square]

      # Update history
      ## Create Move object to capture move data
      self.history.append(move.Move(from_square,to_square, from_piece, to_piece))

      # Update board by replacing elements
      self.array[to_square] = from_piece
      self.array[from_square] = 0

      # Update active_color and move count
      if self.active_color == 'b': 
         self.active_color = 'w'
      else: self.active_color = 'b'
      
      self.full_move += 1
      self.half_move += 1
 
      return self

   def push_san() -> Board:
      #TODO:
      return self
   
   def pop(self) -> str:
      """
      Returns the LAN representation string of the last move pushed.
      """

      # Extract last move from board.history
      try:
         last_move = self.history.pop()
      except Exception as e:
         return []

      from_piece = last_move.from_piece
      from_square = last_move.from_square
      to_piece = last_move.to_piece
      to_square = last_move.to_square
      
      # Revert changes to board elements
      self.array[to_square] = to_piece
      self.array[from_square] = from_piece
      
      # Revert changes to active_color and move count
      if self.active_color == 'b': 
         self.active_color = 'w'
      else: self.active_color = 'b'

      self.full_move += -1
      self.half_move += -1

      return last_move

