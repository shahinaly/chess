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
