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

def node_counter(b      : Board, 
                 depth  : int, 
                 nodes  : int = 0) -> int:
   if depth == 0:
      return nodes + 1
   else:
      candidate_moves = mv.get_all_moves(b)

      for from_square in candidate_moves:
         for move in candidate_moves[from_square]:
            b.push_lan(move)
            nodes = node_counter(b, depth -1, nodes)
            b.pop()
      return nodes

def count_dict(move_dict : Dict) -> int:
   result = 0
   for key in move_dict:
      result += len(move_dict[key])
   return result


def perft(depth   : int,
          fen     : str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> (int, dict):

   board = b.Board(fen = fen)

   nodes_total = 0
   nodes_dict  = {}

   candidate_moves = mv.get_all_moves(board)
   
   for key in candidate_moves.keys():
      for move in candidate_moves[key]:
         board.push_lan(move)
         nodes_dict[move] = node_counter(board,depth)
         nodes_total += nodes_dict[move]
         board.pop()

   return (nodes_total, nodes_dict)
   
