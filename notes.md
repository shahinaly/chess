# 2025-11-26:

A note about the chosen tech: I've chosen to move ahead with python as the primary language for the project. The thinking at this point in time is that I will still get a chance to write C code for the engine while giving me a chance to also learn about integrating the two languages.

## Today's work:
- Board Representation:
  - squares
  - piece type, color, location
  - move count
  - en-passant flag
  - 50 move rule


# 2025-12-05:

I think more thought needs to be given to the class structure of the board. I've chosen to remove the "Piece" class when I began thinking about implementing the board logic. The problem was as follows:
  - Piece objects will be placed at some index in an array.
  - Regardless of whether piece objects contain a location attribute, the board will still have to be passed to LegalMoves()
  - So why not just encode the rank directly into the board array, pass the board, and skip the piece object?
  - The only con of this approach is we miss out on having piece objects contains an array of legal moves particular to that piece.
Perhaps it would be worth thinking ahead instead and trying to predict what functionality my board logic and engine functions will require. Let me start by listing some basic functions they'll likely include and seeing what those functions will need:

## Board Logic:
  - Legal moves for a given piece, side, piece type: The most general way to do this would be have a moves class that has:
    - input: some object representing the game state - either game object or a fen string
    - output: a list of moves in the form of array indices.
Essentially, there should be a board.moves(square) function that generates the legal moves for a particular square.

# 2025-12-16

Worth thinking about smart ways to actually implement a move as it can start to get unruly. Perhaps a good way to start thinking about it that all moves can be
broadly classified as follows:
  - Positioning Move (i.e no capture)
  - Capture
  - Castling
  - Special Pawn Moves
# 2025-12-17
The goal for today is to implement legal moves and have a function for making and unmaking moves.

# 2026-01-27
Debugging.

First bug: Realized this bug while watching sebastian lange's video. Castling rights weren't properly updated after a rook is captured, allowing a king to castle using an opponent's piece.

## Current focus:
  - Position: 8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 b - - 0 2
  - Thinking was the engine allowed en-passants that result in revealed checks. This doesn't happen.
  - In the above position, if we play d5 ("8/8/8/KPpp3r/5p1k/1R6/4P1P1/8 w - c6"), the engine then recognizes the en-passant as a legal move.

