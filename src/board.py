import board_tools as bt
import parse_tools as pt
import move

#TODO:
# push_san(self, san_move : str)

class Board:
   """
   Board object is a container game data and methods to manipulate that data.
   """
   def __init__(
         self, 
         fen:str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):

      (self.fen,
       self.active_color,
       self.castling,
       self.en_passant,
       self.half_move,
       self.full_move) = fen.split()

      self.array = bt.make_board(self.fen)
      self.half_move = int(self.half_move)
      self.full_move = int(self.full_move)
      self.active_color = 1 if self.active_color == 'w' else -1
      self.history = []
      self.white_king, self.black_king = bt.find_kings(self)

   def __str__(self):
      bt.print_board_array(self)
      print("—"*72)

      print(
         "Active color:             " + ('w' if self.active_color == 1 else 'b'),
         "Current Move number:      " + str(self.full_move),
         "Castling:                 " + self.castling,
         "En passant:               " + self.en_passant,
         "FEN:                      " + self.fen,
         sep="\n"
      )
      print("—"*72, end = '')
      return ""

   def push(self, from_square : int, to_square : int) -> Board:
      direction = pt.sgn(self.array[from_square])
      
      ## Create Move object to capture move data
      this_move = move.Move(self, from_square, to_square)
      if bt.is_en_passant(self, from_square, to_square):
         this_move.en_passanted = to_square - direction*move.NORTH
         self.array[to_square - direction*move.NORTH] = 0
      elif bt.is_castling(self, from_square, to_square):
         if from_square < to_square : # King side
            this_move.castle_rook_old = to_square + move.EAST
            this_move.castle_rook_new = to_square + move.WEST

            # Update secondary pieces (rook) when castling
            self.array[to_square + move.WEST] = self.array[to_square + move.EAST]
            self.array[to_square + move.EAST] = 0
         else: # Queen side
            this_move.castle_rook_old = to_square + move.WEST*2
            this_move.castle_rook_new = to_square + move.EAST
            # update secondary pieces (rook) when castling
            self.array[to_square + move.EAST] = self.array[to_square + move.WEST * 2]
            self.array[to_square + move.WEST * 2] = 0
      
      self.history.append(this_move)
      bt.update_meta(self, from_square, to_square)

      # Update board by replacing primary elements
      self.array[to_square] = self.array[from_square]
      self.array[from_square] = 0

      return this_move

   def push_lan(self, lan : str) -> Board: #lan here is long algebraic notation
      from_square, to_square = pt.convert_lan(lan)
      return self.push(from_square, to_square)

   def push_idx(self, from_square : int, to_square : int) -> Board:
      return self.push(from_square, to_square)

   def pop(self) -> str:
      """
         Returns the LAN representation string of the last move pushed.
      """
      
      # Extract last move from board.history
      try:
         last_move = self.history.pop()
      except Exception as e:
         return []

      from_piece  = last_move.from_piece
      from_square = last_move.from_square
      to_piece    = last_move.to_piece
      to_square   = last_move.to_square
      
      # Revert changes to board elements
      self.array[to_square] = to_piece
      self.array[from_square] = from_piece
      
      if last_move.en_passanted :
         # if the last move was an en passant, retrieve the square idx of the
         # en_passanted piece and place a pawn of the opposite color to the 
         # moved piece.
         self.array[last_move.en_passanted] = -1*from_piece
      # Revert changes to active_color and move count
      self.active_color = -1 * self.active_color 
      
      # Update Move Number
      self.half_move += -1
      if self.active_color == -1: self.full_move += -1

      # Revert changes to King location
      if from_piece == 6:
         self.white_king = from_square
      elif from_piece ==  -6:
         self.black_king = from_square

      # Revert changes to en_passant and castling
      self.en_passant = last_move.en_passant
      self.castling   = last_move.castling_rights

      # Move rook back if castling:
      if last_move.castle_rook_new:
         self.array[last_move.castle_rook_old] = self.array[last_move.castle_rook_new]
         self.array[last_move.castle_rook_new] = 0
      return last_move

