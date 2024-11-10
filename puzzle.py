# made with fun! :)
import random 

DIFFICULTY = 50  # Set the number of random moves the puzzle starts with.
SIZE = 4  # Define the board dimensions as NxN.
BLANK = 0 # Define the blank tile
UP = 'up' # Move up
DOWN = 'down' # Move down
LEFT = 'left' # Move left
RIGHT = 'right' # Move right

class Puzzle:
    @staticmethod
    def displayBoard(board):
        """Display the tiles stored in a board on the screen in a bordered format."""
        for y in range(SIZE):
            print('+----' * SIZE + '+')
            for x in range(SIZE):
                if board[y * SIZE + x] == BLANK:
                    print('|    ', end='')
                else:
                    print(f'| {str(board[y * SIZE + x]).rjust(2)} ', end='')
            print('|')
        print('+----' * SIZE + '+')

    @staticmethod
    def getNewBoard():
        """Return a list that represents a new tile puzzle."""
        board = []  # Initialize an empty list for the board.
        for i in range(1, SIZE * SIZE):
            board.append(i)  # Append tile numbers to the board.
        board.append(BLANK)  # Append the blank tile at the end.
        return board

    @staticmethod
    def findBlankSpace(board):
        """Return the coordonates of the blank space's location."""
        for x in range(SIZE):  # Loop through each column.
            for y in range(SIZE):  # Loop through each row.
                if board[y * SIZE + x] == BLANK:  # Check if the current tile is blank.
                    return [x, y]  # Return the coordinates of the blank tile.
                
    @staticmethod
    def makeMove(board, move):
        """Make the move on the board."""
        bx, by = Puzzle.findBlankSpace(board)  # Get the position of the blank tile.
        blankIndex = by * SIZE + bx  # Calculate the index of the blank tile.
        if move == UP:
            tileIndex = (by + 1) * SIZE + bx
        elif move == LEFT:
            tileIndex = by * SIZE + (bx + 1)
        elif move == DOWN:
            tileIndex = (by - 1) * SIZE + bx
        elif move == RIGHT:
            tileIndex = by * SIZE + (bx - 1)
        # Swap the tiles at blankIndex and tileIndex:
        board[blankIndex], board[tileIndex] = board[tileIndex], board[blankIndex]

    # NOTE: this is used for recurrsive DFS
    @staticmethod
    def undoMove(board, move):
        """Do the opposite move of `move` to undo it on `board`."""
        if move == UP:
            Puzzle.makeMove(board, DOWN)
        elif move == DOWN:
            Puzzle.makeMove(board, UP)
        elif move == LEFT:
            Puzzle.makeMove(board, RIGHT)
        elif move == RIGHT:
            Puzzle.makeMove(board, LEFT)

    @staticmethod
    def getValidMoves(board, prevMove=None):
        """Returns a list of the valid moves to make on this board. If
        prevMove is provided, do not include the move that would undo it."""
        blankx, blanky = Puzzle.findBlankSpace(board)
        validMoves = []
        if blanky != SIZE - 1 and prevMove != DOWN:
            validMoves.append(UP)
        if blankx != SIZE - 1 and prevMove != RIGHT:
            validMoves.append(LEFT)
        if blanky != 0 and prevMove != UP:
            validMoves.append(DOWN)
        if blankx != 0 and prevMove != LEFT:
            validMoves.append(RIGHT)
        return validMoves

    @staticmethod
    def getNewPuzzle():
        """Get a new puzzle by making random slides from the solved state."""
        board = Puzzle.getNewBoard()  # Start with a new solved board.
        for i in range(DIFFICULTY):  # Perform a number of random moves to shuffle.
            validMoves = Puzzle.getValidMoves(board)  # Get the valid moves.
            Puzzle.makeMove(board, random.choice(validMoves))  # Randomly make a move.
        return board

    # Heuristic functions to estimate the cost to solve the puzzle.

    # h1: Misplaced Tiles heuristic
    @staticmethod
    def misplacedTiles(board):
        """Count the number of tiles that are not in the goal position."""
        misplaced = 0  # Initialize count of misplaced tiles.
        for i in range(len(board)):  # Loop through each tile in the board.
            if board[i] != BLANK and board[i] != i + 1:  # Check if tile is misplaced.
                misplaced += 1  # Increment the count if it's misplaced.
        return misplaced  # Return the count of misplaced tiles.

    # h2: Euclidean Distance heuristic
    @staticmethod
    def euclideanDistance(board):
        # Σ(sqrt()(x - target_x)² + (y - target_y)²)
        """Calculate the Euclidean distance heuristic."""
        distance = 0  # Initialize total distance to 0.
        for i in range(len(board)):  # Loop through each tile in the board.
            if board[i] != BLANK:  # Ignore the blank tile.
                x, y = divmod(i, SIZE)  # Get current tile's coordinates.
                target_x, target_y = divmod(board[i] - 1, SIZE)  # Get target coordinates.
                distance += ((x - target_x) ** 2 + (y - target_y) ** 2) ** 0.5  # Add Euclidean distance to total.
        return distance
    
    # h3: Manhattan distance heuristic
    @staticmethod
    def manhattanDistance(board):
        # Σ(|x - target_x| + |y - target_y|)
        """Calculate the Manhattan distance heuristic."""
        distance = 0  # Initialize total distance to 0.
        for i in range(len(board)):  # Loop through each tile in the board.
            if board[i] != BLANK:  # Ignore the blank tile.
                x, y = divmod(i, SIZE)  # Get current tile's coordinates.
                target_x, target_y = divmod(board[i] - 1, SIZE)  # Get target coordinates.
                distance += abs(x - target_x) + abs(y - target_y)  # Add the distance to the total.
        return distance 
    
    # h4: Number of tiles out of row and column heuristics
    @staticmethod
    def rowColumnHeuristic(board):
        # (Number of tiles out of row) + (Number of tiles out of column)
        """Calculate the number of tiles out of row and column."""
        out_of_row = 0  # Count of tiles out of their correct row
        out_of_col = 0  # Count of tiles out of their correct column
        for i in range(len(board)):  # Loop through each tile in the board
            if board[i] != BLANK:  # Ignore the blank tile
                x, y = divmod(i, SIZE)  # Current tile's coordinates
                target_x, target_y = divmod(board[i] - 1, SIZE)  # Target coordinates
                if y != target_y: # Check if the tile is out of its row
                    out_of_row += 1
                if x != target_x: # Check if the tile is out of its column
                    out_of_col += 1
        return out_of_row + out_of_col
    
    # h5: Linear Conflict heuristic
    @staticmethod
    def linearConflict(board):
        # Σ(conflicts) + Manhattan Distance
        """Calculate the linear conflict heuristic."""
        conflict = 0  # Initialize conflict count to 0.
        for row in range(SIZE):  # Loop through each row.
            for col in range(SIZE):  # Loop through each column.
                tile = board[row * SIZE + col]  # Get the current tile.
                if tile != BLANK and tile != row * SIZE + col + 1:  # Check if the tile is out of place.
                    target_x, target_y = divmod(tile - 1, SIZE)  # Get target coordinates.
                    if target_y == col:  # If the tile is in the same column.
                        conflict += 2  # Each pair of tiles in conflict adds 2 to the conflict count.
        return conflict + Puzzle.manhattanDistance(board)