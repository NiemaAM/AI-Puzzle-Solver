[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org)

# AI Puzzle Solver Using Python
* The 8-puzzle game, often used as a foundational example to explore search algorithms and heuristics, is a well-known algorithm in artificial intelligence and computer science. 
* The puzzle is a 4x4 grid containing 15 numbered tiles and a blank space allowing adjacent tiles to slide into it.
* The goal is to rearrange the tiles into a fixed goal state from any starting configuration where the tiles are in numerical order with the blank space first. 
* This puzzle is a good study model for heuristic search strategies.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#run-the-project">Run the Project</a>
    </li>
    <li>
      <a href="#puzzle-building">Puzzle Building</a>
      <ul>
        <li><a href="#constants">Constants</a></li>
        <li><a href="#generate-a-new-board">Generate a New Board</a></li>
        <li><a href="#get-moves-on-the-puzzle">Get Moves on the Puzzle</a></li>
      </ul>
    </li>
    <li>
      <a href="#a-star-heuristics">A* Heuristics</a>
      <ul>
        <li><a href="#h1-misplaced-tiles-heuristic">h1: Misplaced Tiles Heuristic</a></li>
        <li><a href="#h2-euclidean-distance-heuristic">h2: Euclidean Distance Heuristic</a></li>
        <li><a href="#h3-manhattan-distance-heuristic">h3: Manhattan Distance Heuristic</a></li>
        <li><a href="#h4-number-of-tiles-out-of-row-and-column-heuristic">h4: Number of Tiles Out of Row and Column Heuristic</a></li>
        <li><a href="#h5-linear-conflict-heuristic">h5: Linear Conflict Heuristic</a></li>
      </ul>
    </li>
    <li>
      <a href="#search-methods">Search Methods</a>
      <ul>
        <li><a href="#a-star-search">A* Search</a></li>
        <li><a href="#dfs-search">DFS Search</a></li>
        <li><a href="#dfs-with-iterative-deepening-search">DFS with Iterative Deepening Search</a></li>
        <li><a href="#bfs-search">BFS Search</a></li>
        <li><a href="#ucs-search">UCS Search</a></li>
      </ul>
    </li>
  </ol>
</details>


## Run the Project
Try the code Online: [HERE](https://nam.neetocode.com/niema-alaoui-mdaghri/01JCBW62Q087G06SXNH2F2XR0D)
Or 
Run the project using command prompt:
```bash
python main.py
```
## Puzzle Building
### Constants
```python
    DIFFICULTY = 50  # Set the number of random moves the puzzle starts with.
    SIZE = 4  # Define the board dimensions as NxN.
    BLANK = 0 # Define the blank tile
    UP = 'up' # Move up
    DOWN = 'down' # Move down
    LEFT = 'left' # Move left
    RIGHT = 'right' # Move right
```
### Generate a new borad
```python
    def getNewBoard():
        """Return a list that represents a new tile puzzle."""
        board = []  # Initialize an empty list for the board.
        for i in range(1, SIZE * SIZE):
            board.append(i)  # Append tile numbers to the board.
        board.append(BLANK)  # Append the blank tile at the end.
        return board
    
    def findBlankSpace(board):
        """Return the coordonates of the blank space's location."""
        for x in range(SIZE):  # Loop through each column.
            for y in range(SIZE):  # Loop through each row.
                if board[y * SIZE + x] == BLANK:  # Check if the current tile is blank.
                    return [x, y]  # Return the coordinates of the blank tile.
```
### Get Moves on the puzzle
```python
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

    def getNewPuzzle():
        """Get a new puzzle by making random slides from the solved state."""
        board = Puzzle.getNewBoard()  # Start with a new solved board.
        for i in range(DIFFICULTY):  # Perform a number of random moves to shuffle.
            validMoves = Puzzle.getValidMoves(board)  # Get the valid moves.
            Puzzle.makeMove(board, random.choice(validMoves))  # Randomly make a move.
        return board
```
### A* Heuristics
### h1: Misplaced Tiles heuristic
```python
    def misplacedTiles(board):
        """Count the number of tiles that are not in the goal position."""
        misplaced = 0  # Initialize count of misplaced tiles.
        for i in range(len(board)):  # Loop through each tile in the board.
            if board[i] != BLANK and board[i] != i + 1:  # Check if tile is misplaced.
                misplaced += 1  # Increment the count if it's misplaced.
        return misplaced  # Return the count of misplaced tiles.
```
### h2: Euclidean Distance heuristic
```python
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
```
### h3: Manhattan distance heuristic
```python
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
```
### h4: Number of tiles out of row and column heuristics
```python
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
```
### h5: Linear Conflict heuristic
```python
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
```
## Search methods
### A* Search
```python
    def Astar(board, heuristic):
        """Use A* to solve the puzzle with the specified heuristic."""
        print(f'\n>>>Attempting to solve the puzzle using A* with {heuristic.__name__}...')
        start_state = tuple(board)
        goal_state = tuple(Puzzle.getNewBoard())

        # Initialize a priority queue with (cost + heuristic, cost so far, moves made, board state)
        timer = time.time()
        priority_queue = []
        heapq.heappush(priority_queue, (0 + heuristic(start_state), 0, [], start_state))
        visited = set()
        expanded_nodes = 0
        max_fringe_size = 0

        while priority_queue:  # While there are states to explore in the queue.
            estimated_cost, cost_so_far, moves_made, current_state = heapq.heappop(priority_queue)  # Pop the state with the lowest cost.
            expanded_nodes += 1  # Increment the expanded nodes counter.
            max_fringe_size = max(max_fringe_size, len(priority_queue))  # Update max fringe size.

            if current_state == goal_state:  # If the current state is the goal state.
                # print the moves made
                for move in moves_made:
                    time.sleep(0.5)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    Puzzle.makeMove(board, move)
                    Puzzle.displayBoard(board)
                    print()
                print('Solved in', len(moves_made), 'moves:')  # Print the number of moves taken to solve.
                print(', '.join(moves_made))  # Print the moves made.
                return True, len(moves_made), expanded_nodes, max_fringe_size, time.time() - timer  # Return success and relevant statistics.

            if current_state in visited:  # If the state has already been visited.
                continue  # Skip to the next state in the queue.
            visited.add(current_state)  # Add the current state to the visited set.

            for move in Puzzle.getValidMoves(current_state):  # For each valid move from the current state.
                new_state = list(current_state)  # Create a new list for the new state.
                Puzzle.makeMove(new_state, move)  # Make the move on the new state.
                new_state_tuple = tuple(new_state)  # Convert the new state to a tuple.
                new_cost = cost_so_far + 1  # Increment the cost of the new state.
                heuristic_value = heuristic(new_state)  # Calculate the heuristic for the new state.

                if new_state_tuple not in visited:  # If the new state has not been visited.
                    # Push the new state into the priority queue with its total cost:
                    heapq.heappush(priority_queue, (new_cost + heuristic_value, new_cost, moves_made + [move], new_state_tuple))

        return False, 0, expanded_nodes, max_fringe_size, time.time() - timer  # Unable to find a solution.
```
### DFS Search
```python
    def DFS(board, timeout=10):
        """Attempt to solve the puzzle using Depth-First Search."""
        print('\n>>> Attempting to solve the puzzle using DFS...')
        start_state = tuple(board)
        goal_state = tuple(Puzzle.getNewBoard())

        timer = time.time()
        stack = [(start_state, [], 0)]
        visited = set()
        expanded_nodes = 0
        max_fringe_size = 0

        while stack:  # While there are states to explore in the stack
            # Check for timeout
            if time.time() - timer > timeout:
                print("Timeout")
                return False, 0, expanded_nodes, max_fringe_size, time.time() - timer
            
            current_state, moves_made, depth = stack.pop()  # Pop the last state from the stack
            expanded_nodes += 1  # Increment the expanded nodes counter

            # Update max fringe size
            max_fringe_size = max(max_fringe_size, len(stack))

            if current_state == goal_state:  # If the current state is the goal state
                # print the moves made
                for move in moves_made:
                    time.sleep(0.5)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    Puzzle.makeMove(board, move)
                    Puzzle.displayBoard(board)
                    print()
                print('Solved in', len(moves_made), 'moves:')  # Print the number of moves taken to solve
                print(', '.join(moves_made))  # Print the moves made
                return True, len(moves_made), expanded_nodes, max_fringe_size, time.time() - timer  # Return success and relevant statistics

            if current_state in visited:  # If the state has already been visited
                continue  # Skip to the next state in the stack
            visited.add(current_state)  # Add the current state to the visited set

            for move in Puzzle.getValidMoves(current_state):  # For each valid move from the current state
                new_state = list(current_state)  # Create a new list for the new state
                Puzzle.makeMove(new_state, move)  # Make the move on the new state
                new_state_tuple = tuple(new_state)  # Convert the new state to a tuple

                if new_state_tuple not in visited:  # If the new state has not been visited
                    # Push the new state onto the stack with its moves
                    stack.append((new_state_tuple, moves_made + [move], depth + 1))

        return False, 0, expanded_nodes, max_fringe_size, time.time() - timer  # Unable to find a solution
```
### DFS with itterative deepening Search
```python
    def DFSR(board, maxMoves=10):
        """Attempt to solve the puzzle in `board` in at most `maxMoves` moves."""
        print('\n>>>Attempting to solve the puzzle using Recursive DFS in at most', maxMoves, 'moves...')
        
        timer = time.time()
        moves_made = []
        expanded_nodes = 0 
        max_fringe_size = 0
        solved = Search.backtrack(board, moves_made, maxMoves, None)
        
        if solved:
            # print the moves made
            for move in moves_made:
                time.sleep(0.5)
                os.system('cls' if os.name == 'nt' else 'clear')
                Puzzle.makeMove(board, move)
                Puzzle.displayBoard(board)
                print()
            print('Solved in', len(moves_made), 'moves:')  # Print the number of moves taken to solve
            print(', '.join(moves_made))  # Print the moves made
            return True, len(moves_made), expanded_nodes, max_fringe_size, time.time() - timer # Puzzle was solved.
        else:
            return False, len(moves_made), expanded_nodes, max_fringe_size, time.time() - timer # Unable to solve in maxMoves moves.
    
    # backtrack
    def backtrack(board, movesMade, movesRemaining, prevMove):
        """A recursive function that attempts all possible moves until 
        it finds a solution or reaches the maxMoves limit."""
        if movesRemaining < 0:
            # BASE CASE - Ran out of moves.
            return False
        if board == Puzzle.SOLVED_BOARD:
            # BASE CASE - Solved the puzzle.
            return True
        # RECURSIVE CASE - Attempt each of the valid moves:
        for move in Puzzle.getValidMoves(board, prevMove):
            # Make the move:
            Puzzle.makeMove(board, move)
            movesMade.append(move)
            if Search.backtrack(board, movesMade, movesRemaining - 1, move):
                # If the puzzle is solved, return True:
                Puzzle.undoMove(board, move) # Reset to the original puzzle.
                return True
            # Undo the move to set up for the next move:
            Puzzle.undoMove(board, move)
            movesMade.pop() # Remove the last move since it was undone.
        return False # BASE CASE - Unable to find a solution.
```
### BFS Search
```python
    def BFS(board, timeout=10):
        """Attempt to solve the puzzle using Breadth-First Search."""
        print('\n>>>Attempting to solve the puzzle using BFS...')
        start_state = tuple(board)
        goal_state = tuple(Puzzle.getNewBoard())

        # Initialize a queue with (board state, moves made, depth).
        timer = time.time()
        queue = deque([(start_state, [], 0)])  
        visited = set()
        expanded_nodes = 0
        max_fringe_size = 0

        while queue:  # While there are states to explore in the queue.
            # Check for timeout
            if time.time() - timer > timeout:
                print("Timeout")
                return False, 0, expanded_nodes, max_fringe_size, time.time() - timer
            
            current_state, moves_made, depth = queue.popleft()  # Dequeue the state.
            expanded_nodes += 1  # Increment the expanded nodes counter.

            # Update max fringe size
            max_fringe_size = max(max_fringe_size, len(queue))

            if current_state == goal_state:  # If the current state is the goal state.
                # print the moves made
                for move in moves_made:
                    time.sleep(0.5)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    Puzzle.makeMove(board, move)
                    Puzzle.displayBoard(board)
                    print()
                print('Solved in', len(moves_made), 'moves:')  # Print the number of moves taken to solve.
                print(', '.join(moves_made))  # Print the moves made.
                return True, len(moves_made), expanded_nodes, max_fringe_size, time.time() - timer  # Return success and relevant statistics.

            if current_state in visited:  # If the state has already been visited.
                continue  # Skip to the next state in the queue.
            visited.add(current_state)  # Add the current state to the visited set.

            for move in Puzzle.getValidMoves(current_state):  # For each valid move from the current state.
                new_state = list(current_state)  # Create a new list for the new state.
                Puzzle.makeMove(new_state, move)  # Make the move on the new state.
                new_state_tuple = tuple(new_state)  # Convert the new state to a tuple.

                if new_state_tuple not in visited:  # If the new state has not been visited.
                    # Enqueue the new state with its moves and increment depth:
                    queue.append((new_state_tuple, moves_made + [move], depth + 1))

        return False, 0, expanded_nodes, max_fringe_size, time.time() - timer  # Unable to find a solution.
```
### UCS Search
```python
    def UCS(board, timeout=10):
        """Attempt to solve the puzzle using Uniform-Cost Search."""
        print('\n>>>Attempting to solve the puzzle using UCS...')
        start_state = tuple(board)
        goal_state = tuple(Puzzle.getNewBoard())

        timer = time.time()
        priority_queue = [(0, start_state, [], 0)]
        visited = set()
        expanded_nodes = 0
        max_fringe_size = 0 

        while priority_queue:  # While there are states to explore in the queue
            # Check for timeout
            if time.time() - timer > timeout:
                print("Timeout")
                return False, 0, expanded_nodes, max_fringe_size, time.time() - timer
            
            cost_so_far, current_state, moves_made, depth = heapq.heappop(priority_queue)  # Pop the state with the lowest cost
            expanded_nodes += 1  # Increment the expanded nodes counter
            max_fringe_size = max(max_fringe_size, len(priority_queue))  # Update max fringe size

            if current_state == goal_state:  # If the current state is the goal state
                # print the moves made
                for move in moves_made:
                    time.sleep(0.5)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    Puzzle.makeMove(board, move)
                    Puzzle.displayBoard(board)
                    print()
                print('Solved in', len(moves_made), 'moves:')  # Print the number of moves taken to solve
                print(', '.join(moves_made))  # Print the moves made
                return True, len(moves_made), expanded_nodes, max_fringe_size, time.time() - timer  # Return success and relevant statistics

            if current_state in visited:  # If the state has already been visited
                continue  # Skip to the next state in the queue
            visited.add(current_state)  # Add the current state to the visited set

            for move in Puzzle.getValidMoves(current_state):  # For each valid move from the current state
                new_state = list(current_state)  # Create a new list for the new state
                Puzzle.makeMove(new_state, move)  # Make the move on the new state
                new_state_tuple = tuple(new_state)  # Convert the new state to a tuple
                new_cost = cost_so_far + 1  # Increment the cost of the new state

                if new_state_tuple not in visited:  # If the new state has not been visited
                    # Push the new state into the priority queue with its total cost:
                    heapq.heappush(priority_queue, (new_cost, new_state_tuple, moves_made + [move], depth + 1))

        return False, 0, expanded_nodes, max_fringe_size, time.time() - timer  # Unable to find a solution
```