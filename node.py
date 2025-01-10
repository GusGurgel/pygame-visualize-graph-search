from settings import *
from math import sqrt

class Node:
    # Default functions
    cost_function = "c1"
    heuristic_function = "h1"

    # Variable for A* search
    use_a_star_compration = False
    a_start_objective_node = None

    def __init__(self, pos, cost=0, parrent=None):
        self.pos = pos  # node position
        self.cost = cost  # cost to node
        self.parrent = parrent  # node parent

        # Calculate node path
        if self.parrent == None:
            self.path = [self.pos]
        else:
            self.path = parrent.path + [self.pos]

        # Calculate node depth
        if self.parrent == None:
            self.depth = 0
        else:
            self.depth = self.parrent.depth + 1

        # Calculate accumulate cost
        if parrent == None:
            self.accumulate_cost = self.cost + 0
        else:
            self.accumulate_cost = self.cost + parrent.accumulate_cost

    def get_neighbors(self):
        costs = []
        neighbors = []
        if Node.cost_function == "c1":
            # Todas tem custo 10
            costs = [10] * 4
        elif Node.cost_function == "c2":
            # f1, f2 tem custo 15
            # f3, f4 tem custo 10
            costs = [15] * 2 + [10] * 2
        elif Node.cost_function == "c3":
            # t = profundidade do nó
            # f1, f2 tem custo 10 + (|5-t| mod 6)
            # f3, f4 tem custo 10
            costs =  [10 + (abs(5 - (self.depth + 1)) % 6)] * 2 + [10] * 2
        elif Node.cost_function == "c4":
            # f1, f2 tem custo 5 + (|10-t| mod 11)
            # f3, f4 tem custo 10
            costs =  [5 + (abs(10 - (self.depth + 1)) % 11)] * 2 + [10] * 2
        else:
            raise Exception(f"Invalid cost function -> {Node.cost_function}")
        
        for i in range(len(ACTIONS)):
            neighbor_pos = ACTIONS[i](self.pos)
            neighbor_cost = costs[i]
            neighbor = Node(neighbor_pos, neighbor_cost, self)
            if neighbor.is_valid():
                neighbors.append(neighbor)
        
        return neighbors
    
    def get_heuristic_value(self, other):
        if Node.heuristic_function == "h1":
            # Euclidean Distance
            d_x = pow(abs(other.pos[0] - self.pos[0]), 2)
            d_y = pow(abs(other.pos[1] - self.pos[1]), 2)
            return 10 * sqrt(d_x + d_y)
        elif Node.heuristic_function == "h2":
            # Manhattan Distance
            d_x = abs(other.pos[0] - self.pos[0])
            d_y = abs(other.pos[1] - self.pos[1])
            return 10 * (d_x + d_y)
        else:
            raise Exception(f"Invalid heuristic function -> {Node.cost_function}")
    
    def is_valid(self):
        for i in range(2):
            if self.pos[i] < 0 or self.pos[i] > MAP_SIZE:
                return False
        return True

    def __gt__(self, other):
        if Node.use_a_star_compration and Node.a_start_objective_node != None:
            self_cost = self.accumulate_cost + self.get_heuristic_value(Node.a_start_objective_node)
            other_cost = other.accumulate_cost + other.get_heuristic_value(Node.a_start_objective_node)
            return self_cost > other_cost
        else:
            return self.accumulate_cost > other.accumulate_cost

    def __lt__(self, other):
        if Node.use_a_star_compration and Node.a_start_objective_node != None:
            self_cost = self.accumulate_cost + self.get_heuristic_value(Node.a_start_objective_node)
            other_cost = other.accumulate_cost + other.get_heuristic_value(Node.a_start_objective_node)
            return self_cost < other_cost
        else:
            return self.accumulate_cost < other.accumulate_cost

    def __str__(self):
        return f"pos: {self.pos}, depth: {self.depth}, cost: {self.cost}, "