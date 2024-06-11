import heapq
import copy

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.cost = cost
        self.heuristic = self.calculate_heuristic()

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def calculate_heuristic(self):
        # Manhattan distance heuristic
        goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        h = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:
                    goal_i, goal_j = divmod(self.state[i][j] - 1, 3)
                    h += abs(i - goal_i) + abs(j - goal_j)
        return h

    def get_children(self):
        children = []
        zero_i, zero_j = None, None
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    zero_i, zero_j = i, j
                    break
            if zero_i is not None:
                break

        for move_i, move_j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_i, new_j = zero_i + move_i, zero_j + move_j
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = copy.deepcopy(self.state)
                new_state[zero_i][zero_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_i][zero_j]
                children.append(PuzzleNode(new_state, self, (new_i, new_j), self.cost + 1))

        return children

    def is_goal(self):
        return self.state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def get_path(self):
        path = []
        current = self
        while current is not None:
            path.append((current.move, current.state, current.cost))
            current = current.parent
        path.reverse()
        return path

def solve_puzzle(initial_state):
    start_node = PuzzleNode(initial_state)
    open_set = [start_node]
    heapq.heapify(open_set)
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)
        if current_node.is_goal():
            return current_node.get_path()
        closed_set.add(tuple(map(tuple, current_node.state)))

        for child in current_node.get_children():
            if tuple(map(tuple, child.state)) not in closed_set:
                heapq.heappush(open_set, child)

    return None

# Example usage
initial_state = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
solution = solve_puzzle(initial_state)
if solution:
    for move, state, cost in solution:
        print(f"Move {move}, Cost {cost}:")
        for row in state:
            print(row)
        print()
else:
    print("No solution found.")
