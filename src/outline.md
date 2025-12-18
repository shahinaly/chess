# Essential Elements

Rough Outline of things that need to happen:

1. (FEN to Board) Game Representation (Abstraction)
    - ~Board Representation~
      - ~64 squares~
      - ~piece type, color, and location~
    - ~move count (turn to play)~
    - ~en-passant flag~
    - ~50 move rule flag~
2. Game Logic (Essential Functions)
    - Find Moves
      - Legal moves for pieces
      - ~Regular moves for pawns~
      - en-passant
      - Castling
    - Make mov
    - Unmake move
    - In check?
    - Promote
