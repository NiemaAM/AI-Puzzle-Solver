import csv
from puzzle import Puzzle
from search import Search

NUM_SCENARIOS = 5
DIFFICULTY = 50 

def generate_scenarios(filename, num_scenarios):
    """Generate random puzzle scenarios and save them to a CSV file."""
    scenarios = []
    for _ in range(num_scenarios):
        puzzle = Puzzle.getNewPuzzle()
        scenarios.append(puzzle)
    # Save scenarios to CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for scenario in scenarios:
            writer.writerow(scenario)

def load_scenarios(filename):
    """Load scenarios from a CSV file."""
    scenarios = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            scenarios.append(list(map(int, row)))
    return scenarios

def run_searches(scenarios):
    """Run different search algorithms on the given scenarios and collect results."""
    results = []
    heuristics = [
        Puzzle.misplacedTiles,
        Puzzle.euclideanDistance,
        Puzzle.manhattanDistance,
        Puzzle.rowColumnHeuristic,
        Puzzle.linearConflict
    ]
    for scenario in scenarios:
        result = {'scenario': scenario}
    
        # Run A* for each heuristic
        for heuristic in heuristics:
            puzzle_copy = list(scenario)
            solved, depth, expanded_nodes, max_fringe_size, timer = Search.Astar(puzzle_copy, heuristic)
            result[f'Astar_{heuristic.__name__}'] = (solved, depth, expanded_nodes, max_fringe_size, timer)

        # Run DFS
        puzzle_copy = list(scenario)
        solved, depth, expanded_nodes, max_fringe_size, timer = Search.DFS(puzzle_copy)
        result['DFS'] = (solved, depth, expanded_nodes, max_fringe_size, timer)
        
        # Run BFS
        puzzle_copy = list(scenario)
        solved, depth, expanded_nodes, max_fringe_size, timer = Search.BFS(puzzle_copy)
        result['BFS'] = (solved, depth, expanded_nodes, max_fringe_size, timer)
        
        # Run UCS
        puzzle_copy = list(scenario)
        solved, depth, expanded_nodes, max_fringe_size, timer = Search.UCS(puzzle_copy)
        result['UCS'] = (solved, depth, expanded_nodes, max_fringe_size, timer)

        results.append(result)
    return results

def save_results(filename, results):
    """Save search results to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['Scenario', 'Algorithm', 'Solved', 'Moves', 'Expanded_Nodes', 'Max_Fringe_Size', 'Time']
        writer.writerow(header)

        for result in results:
            scenario = result['scenario']
            
            # Prepare A* results
            for heuristic in ['misplacedTiles', 'euclideanDistance', 'manhattanDistance', 'rowColumnHeuristic', 'linearConflict']:
                key = f'Astar_{heuristic}'
                if key in result:
                    solved, depth, expanded_nodes, max_fringe_size, timer = result[key]
                    row = [scenario, f'A* ({heuristic})', solved, depth, expanded_nodes, max_fringe_size, timer]
                    writer.writerow(row)

            # Prepare DFS results
            if 'DFS' in result:
                solved, depth, expanded_nodes, max_fringe_size, timer = result['DFS']
                row = [scenario, 'DFS', solved, depth, expanded_nodes, max_fringe_size, timer]
                writer.writerow(row)

            # Prepare BFS results
            if 'BFS' in result:
                solved, depth, expanded_nodes, max_fringe_size, timer = result['BFS']
                row = [scenario, 'BFS', solved, depth, expanded_nodes, max_fringe_size, timer]
                writer.writerow(row)

            # Prepare UCS results
            if 'UCS' in result:
                solved, depth, expanded_nodes, max_fringe_size, timer = result['UCS']
                row = [scenario, 'UCS', solved, depth, expanded_nodes, max_fringe_size, timer]
                writer.writerow(row)

def calculate_average(filename):
    """Calculate the average of each search method's results from results.csv and save to Average.csv."""
    averages = {
        'A* (misplacedTiles)': [0, 0, 0, 0, 0],  # solved, depth, expanded_nodes, max_fringe_size, timer
        'A* (euclideanDistance)': [0, 0, 0, 0, 0],
        'A* (manhattanDistance)': [0, 0, 0, 0, 0],
        'A* (rowColumnHeuristic)': [0, 0, 0, 0, 0],
        'A* (linearConflict)': [0, 0, 0, 0, 0],
        'DFS': [0, 0, 0, 0, 0],
        'BFS': [0, 0, 0, 0, 0],
        'UCS': [0, 0, 0, 0, 0]
    }
    
    counts = {
        'A* (misplacedTiles)': 0,
        'A* (euclideanDistance)': 0,
        'A* (manhattanDistance)': 0,
        'A* (rowColumnHeuristic)': 0,
        'A* (linearConflict)': 0,
        'DFS': 0,
        'BFS': 0,
        'UCS': 0
    }

    # Load results from the CSV file
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header
        
        for row in reader:
            algorithm = row[1]
            solved = row[2] == 'True'  # Convert 'True'/'False' to boolean
            depth = int(row[3])
            expanded_nodes = int(row[4])
            max_fringe_size = int(row[5])
            timer = float(row[6])

            if solved:  # Only count solved puzzles for averages
                averages[algorithm][0] += 1  # Increment solved count
                averages[algorithm][1] += depth
                averages[algorithm][2] += expanded_nodes
                averages[algorithm][3] += max_fringe_size
                averages[algorithm][4] += timer
                counts[algorithm] += 1

    # Calculate the averages
    for key in averages.keys():
        if counts[key] > 0:
            averages[key] = [x / counts[key] for x in averages[key]]

    # Save averages to Average.csv
    with open('average.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['Algorithm', 'Average_Solved', 'Average_Depth', 'Average_Expanded_Nodes', 'Average_Max_Fringe_Size', 'Average_Time']
        writer.writerow(header)
        for key in averages.keys():
            writer.writerow([key] + averages[key])

def main():
    # Generate scenarios
    generate_scenarios('scenarios.csv', NUM_SCENARIOS)
    # Load scenarios
    scenarios = load_scenarios('scenarios.csv')
    # Run searches on scenarios
    results = run_searches(scenarios)
    # Save results
    save_results('results.csv', results)
    # Calculate and save averages from results.csv
    calculate_average('results.csv')

if __name__ == '__main__':
    main()
