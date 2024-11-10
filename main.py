import os
from puzzle import Puzzle
from search import Search

def runAstar(puzzleBoard, heuristic):
    puzzleCopy = list(puzzleBoard) 
    solved, depth, expanded_nodes, max_fringe_size, timer = Search.Astar(puzzleCopy, heuristic)
    print(f'Depth of solution: {depth}')
    print(f'Expanded nodes: {expanded_nodes}') 
    print(f'Max fringe size: {max_fringe_size}')  
    print('Run in', round(timer, 3), 'seconds.') 

def runBFS(puzzleBoard):
    puzzleCopy = list(puzzleBoard) 
    solved, depth, expanded_nodes, max_fringe_size, timer = Search.BFS(puzzleCopy)
    print(f'Depth of solution: {depth}')
    print(f'Expanded nodes: {expanded_nodes}') 
    print(f'Max fringe size: {max_fringe_size}')  
    print('Run in', round(timer, 3), 'seconds.') 

def runUCS(puzzleBoard):
    puzzleCopy = list(puzzleBoard) 
    solved, depth, expanded_nodes, max_fringe_size, timer = Search.UCS(puzzleCopy)
    print(f'Depth of solution: {depth}')
    print(f'Expanded nodes: {expanded_nodes}') 
    print(f'Max fringe size: {max_fringe_size}')  
    print('Run in', round(timer, 3), 'seconds.') 

def runDFSR(puzzleBoard):
    puzzleCopy = list(puzzleBoard) 
    maxMoves = 10
    while True:
        solved, depth, expanded_nodes, max_fringe_size, timer = Search.DFSR(puzzleCopy, maxMoves)
        if solved: break
        maxMoves += 1
    print(f'Depth of solution: {depth}')
    print(f'Expanded nodes: {expanded_nodes}') 
    print(f'Max fringe size: {max_fringe_size}')  
    print('Run in', round(timer, 3), 'seconds.')  

def runDFS(puzzleBoard):
    puzzleCopy = list(puzzleBoard) 
    solved, depth, expanded_nodes, max_fringe_size, timer = Search.DFS(puzzleCopy)
    print(f'Depth of solution: {depth}')
    print(f'Expanded nodes: {expanded_nodes}') 
    print(f'Max fringe size: {max_fringe_size}')  
    print('Run in', round(timer, 3), 'seconds.') 

if __name__ == "__main__": 
    os.system('cls' if os.name == 'nt' else 'clear') 
    Puzzle.SOLVED_BOARD = Puzzle.getNewBoard()
    # Generate a shuffled puzzle
    print ("Innitial Puzzle State:")
    puzzleBoard = Puzzle.getNewPuzzle()
    Puzzle.displayBoard(puzzleBoard)
    # heuristics for A*
    heuristics = [
        Puzzle.misplacedTiles,
        Puzzle.euclideanDistance,
        Puzzle.manhattanDistance,
        Puzzle.rowColumnHeuristic,
        Puzzle.linearConflict
    ]
    # menu
    while True:
        print("\nSelect an algorithm to run:")
        print("1. A* Search")
        print("2. Breadth-First Search (BFS)")
        print("3. Uniform Cost Search (UCS)")
        print("4. Depth-First Search (DFS)")
        print("5. Depth-First Search with Recursion Limit (DFSR)")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            print("\nSelect a heuristic for A* Search:")
            print("1. Misplaced Tiles")
            print("2. Euclidean Distance")
            print("3. Manhattan Distance")
            print("4. Row-Column Heuristic")
            print("5. Linear Conflict")
            heuristic_choice = int(input("Enter your choice (1-5): "))
            heuristic = heuristics[heuristic_choice - 1]
            runAstar(puzzleBoard, heuristic)
        elif choice == '2':
            runBFS(puzzleBoard)
        elif choice == '3':
            runUCS(puzzleBoard)
        elif choice == '4':
            runDFS(puzzleBoard)
        elif choice == '5':
            runDFSR(puzzleBoard)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
