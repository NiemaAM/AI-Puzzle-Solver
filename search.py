import os
from puzzle import Puzzle
import time 
from collections import deque
import heapq

class Search:
    # A* solution with a chosen heuristic
    @staticmethod
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
    
    # BFS
    @staticmethod
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
    
    # DFS - normal
    @staticmethod
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
    
    # UCS
    @staticmethod
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
 
    # DFS - itterative deepening
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