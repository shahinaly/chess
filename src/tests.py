from helpers import *

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

