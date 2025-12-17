from helpers import *

# Print grid of squares with alegbraic values and convert back to check convert_loc() works

def test_convert_loc():
   for i in range(100):
      print(f"{convert_loc(i)}",end = ' ')
      if (i+1) % 10 == 0:
         print("\n",end='')
   print("---------------------------")
   for i in range(100):
      print(f"{convert_loc(convert_loc(i))}",end = ' ')
      if (i+1) % 10 == 0:
         print("\n",end='')

