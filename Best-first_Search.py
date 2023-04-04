import queue

# Node class
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, f=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.f = f

    def __lt__(self, other):
        return self.f < other.f

# Best First Search algorithm function
def best_first_search(problem, f):
    # Create a node with the initial state
    node = Node(problem.initial_state())

    # Create a frontier priority queue, ordered by f with node as an element
    frontier = queue.PriorityQueue()
    frontier.put(node)

    # Create a reached dictionary, with an entry with key problem.initial_state() and value node
    reached = {problem.initial_state(): node}

    # While frontier is not empty
    while not frontier.empty():
        # Pop the node with the lowest f-value from frontier
        node = frontier.get()

        # Check if node is a goal state
        if problem.is_goal(node.state):
            return node

        # Expand the node and add its children to the frontier and reached dictionary
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                child.f = f(child)
                frontier.put(child)

    # Return failure if goal not found
    return None

# Expand function
def expand(problem, node):
    # Get the state of the node
    s = node.state

    # For each action in problem.actions(s)
    for action in problem.actions(s):
        # Get the resulting state and cost of the action
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)

        # Create a new child node
        child = Node(state=s1, parent=node, action=action, path_cost=cost)

        # Yield the child node
        yield child

# Test the algorithm with the Romania problem
class Problem:
    def __init__(self, initial_state, goal_state, actions, result, action_cost):
        self.initial_state = lambda: initial_state
        self.is_goal = lambda s: s == goal_state
        self.actions = lambda s: actions[s]
        self.result = lambda s, a: result[s][a]
        self.action_cost = lambda s, a, s1: action_cost[s][a][s1]

# Define the Romania problem
romania_map = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Vaslui': 142, 'Hirsova': 98},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}