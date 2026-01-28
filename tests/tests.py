import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join('..', 'src')))

from parse_tools import convert_loc
import board_tools as bt
import board as b
import move as mv
import parse_tools as pt


# Print grid of squares with alegbraic values and convert back to check convert_loc() works

def test_convert_loc():
   for i in range(144):
      print(f"{convert_loc(i):4s}",end = ' ')
      if (i+1) % 12 == 0:
         print("\n",end='')
   print("---------------------------")
   for i in range(144):
      j = convert_loc(i)
      print(f"{convert_loc(j):4d}",end = ' ')
      #print(f"{convert_loc(convert_loc(i)):03d}",end = ' ')
      if (i+1) % 12 == 0:
         print("\n",end='')

def node_counter(b : Board, depth : int, 
                 nodes        : int = 0, 
                 captures     : int = 0, 
                 enpassants   : int = 0, 
                 castlings    : int = 0,
                 checks       : int = 0) -> int:
   if depth == 0:
      if mv.in_check(b):
         return [nodes + 1, captures, enpassants, castlings, checks + 1]
      else:
         return [nodes + 1, captures, enpassants, castlings, checks]
   else:
      candidate_moves = mv.get_all_moves(b)

      for piece in candidate_moves:
         for target in candidate_moves[piece]:
            new_move = piece + target
            if bt.is_capture(b, pt.convert_loc(piece), pt.convert_loc(target)) and (depth - 1 == 0):
               captures += 1
            elif bt.is_en_passant(b, pt.convert_loc(piece), pt.convert_loc(target)) and (depth -1 == 0):
               enpassants += 1
            elif bt.is_castling(b, pt.convert_loc(piece), pt.convert_loc(target)) and (depth -1 == 0):
               castlings += 1
            b.push_lan(new_move)
            nodes, captures, enpassants, castlings, checks = node_counter(b, depth -1, nodes, captures, enpassants, castlings, checks)
            b.pop()

      return [nodes, captures, enpassants, castlings, checks]

def count_dict(move_dict : Dict) -> int:
   result = 0
   for key in move_dict:
      result += len(move_dict[key])
   return result
