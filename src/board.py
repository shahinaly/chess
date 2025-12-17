class Board:
   def __init__(self, fen):
      self.fen = fen
      self.array = make_board(fen)
   
   def __str__(self):
      # To print the board in a standard format, we must go in the following order:
      # 81...88/.../11...18
      for rank in reversed(range(10)):
         for file in range(10):
            square = rank*10 + file # for when I mess up coorddinates, inevitably

            # print empty squares as '_'
            if self.array[square] == 0:
               print("_", end ='')
            # else, print non-None values
            elif self.array[square] is not None: 
               print(piece_rep(self.array[square]), end = '')
            # Newline after 8 files, exlcuding boundary squares
            if(file == 8 and (rank) != 0 and rank != 9): 
               print("\n", end = '')
      return ""

def make_board(fen : str):
   """
   Accepts a FEN string and returns a 10x10 1D array board
   representation with boreder padding.
   """
   result = [None] * 11
   rows = fen.split('/')
   rows = reversed(rows)
   for row in rows:
      for char in row:
         if char.isdigit():                           # add empty squares
            result.extend([0]*int(char))
         else:                                        # add pieces
            result.append(piece_rep(char))
      result.extend([None]*2)
   result = result + [None] * 11     # add 0 and 9th row padding
   return result

def piece_rep(piece):
   """ 
   converts between character and integer represenation
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
