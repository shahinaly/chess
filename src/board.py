class Board:
   def __init__(self, fen):
      self.fen = fen
      self.array = make_board(fen)
   
   def __str__(self):
      for i in reversed(range(64)):
         if ((i + 1) % 8) == 0 : print("\n",end='')
         if self.array[i] == None : print("_", end='')
         else : print(piece_rep(self.array[i]), end = '')
      return "\n"

def make_board(fen : str):
   result = []
   fen = fen.replace('/','')

   for char in fen:
      if char.isdigit():
         for j in range(int(char)): result.append(None)
      else:
         result.append(piece_rep(char))
   return result

def piece_rep(piece):
   """ If piece is """
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

