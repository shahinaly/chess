def convert_loc(loc):
   """
   Converts between 1D array board representation index and algebraic notation
   """
   files = 'yzabcdefghij'

   if type(loc) is int :
      rank = (loc // 12) - 1                           # e.g loc 53 => rank 5 on a 10x10 board
      file = files[(loc - 12 * (rank + 1))]              # e.g loc 53 => file = 53 - 5*10
      return file + str(rank)

   elif type(loc) is str :
      rank = int(loc[1:]) + 1
      file = files.index(loc[0])
      return rank*12 + file

def sgn(piece : int):
   """
   Accepts a piece representation and returns 1 or -1 depending on the color.
   In place in case piece implementation changes but board representation stays the same.
   """
   # Current implementation of pieces is 1..6 for P...K with black pieces being negative
   if piece < 0: return -1
   elif piece > 0: return  1
   elif piece == 0: return 0
   else: return None


