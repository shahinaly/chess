def convert_loc(loc):
   """
   Converts between 1D array board representation index and algebraic notation
   """
   files = 'zabcdefghi'

   if type(loc) is int :
      rank = loc // 10                          # e.g loc 53 => rank 5 on a 10x10 board
      file = files[(loc - 10 * rank)]             # e.g loc 53 => file = 53 - 5*10
      return file + str(rank)

   elif type(loc) is str :
      rank = int(loc[1])
      file = files.index(loc[0])
      loc = str(rank) + str(file)   # 'a5' equivalent to 51 
      return int(loc)

def sgn(piece : int):
   """
   Accepts a piece representation and returns 1 or -1 depending on the color.
   In place in case piece implementation changes but board representation stays the same.
   """
   # Current implementation of pieces is 1..6 for P...K with black pieces being negative
   if piece < 0: return -1
   elif piece > 0: return  1

def valid_target_square(piece : int, target_square : int):
   """
      Returns a boolean depending on whether a given target square is valid for a piece 
      to move to or to capture.
   """
   if (target_square is None) or sgn(piece) == sgn(target_square):
      return False
   else:
      return True

