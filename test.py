import os
from puzzle import Puzzle
from search import Search

if __name__ == "__main__": 
    os.system('cls' if os.name == 'nt' else 'clear') 

    Puzzle.SOLVED_BOARD = Puzzle.getNewBoard()
    
    # Generate a shuffled puzzle
    print ("Innitial Puzzle State:")
    puzzleBoard = Puzzle.getNewPuzzle()
    Puzzle.displayBoard(puzzleBoard)

    heuristics = [
        Puzzle.misplacedTiles,
        Puzzle.euclideanDistance,
        Puzzle.manhattanDistance,
        Puzzle.rowColumnHeuristic,
        Puzzle.linearConflict
    ]

    # A*
    for heuristic in heuristics:
        puzzleCopy = list(puzzleBoard) 
        solved, depth, expanded_nodes, max_fringe_size, timer = Search.Astar(puzzleCopy, heuristic)
        print(f'Depth of solution: {depth}')
        print(f'Expanded nodes: {expanded_nodes}') 
        print(f'Max fringe size: {max_fringe_size}')  
        print('Run in', round(timer, 3), 'seconds.') 

    # DFS
    puzzleCopy = list(puzzleBoard) 
    solved, depth, expanded_nodes, max_fringe_size, timer = Search.DFS(puzzleCopy)
    print(f'Depth of solution: {depth}')
    print(f'Expanded nodes: {expanded_nodes}') 
    print(f'Max fringe size: {max_fringe_size}')  
    print('Run in', round(timer, 3), 'seconds.') 

    # BFS
    puzzleCopy = list(puzzleBoard) 
    solved, depth, expanded_nodes, max_fringe_size, timer = Search.BFS(puzzleCopy)
    print(f'Depth of solution: {depth}')
    print(f'Expanded nodes: {expanded_nodes}') 
    print(f'Max fringe size: {max_fringe_size}')  
    print('Run in', round(timer, 3), 'seconds.') 

    # UCS
    puzzleCopy = list(puzzleBoard) 
    solved, depth, expanded_nodes, max_fringe_size, timer = Search.UCS(puzzleCopy)
    print(f'Depth of solution: {depth}')
    print(f'Expanded nodes: {expanded_nodes}') 
    print(f'Max fringe size: {max_fringe_size}')  
    print('Run in', round(timer, 3), 'seconds.') 
""" 
    # DFSR
    # NOTE: backtraking with DFS
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
"""