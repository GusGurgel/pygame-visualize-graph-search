from settings import *
from queue import PriorityQueue
import heapq
from node import *
from cell import *

class Grid():
    def __init__(self, all_sprites):
        self.cells_matrix = []
        for i in range(MAP_SIZE+1):
            self.cells_matrix.append([])
        for i in range(MAP_SIZE+1):
            for j in range(MAP_SIZE+1):
                self.cells_matrix[i].append(Cell((i, j), all_sprites))

        self.search_step_coldown = START_CELL_STEP_COLDOWN
        self.search_step_clock = 0
        self.search_step_started = False
        self.make_step = False
        self.make_path_clock = 0
        self.make_path_coldown = MAKE_PATH_COLDOWN
    
        self.search_running = False
        self.search_end = True
        self.search_algorithm = SEARCH_ALGORITHMS[0]
        Node.cost_function = NODE_COST_FUNCTIONS[0]
        Node.heuristic_function = NODE_HEURISTIC_FUNCTIONS[0]

        self.inital_pos = (15, 15)
        self.objetive_pos = (15, 16)
        self.current_node = None
        self.result_node = None
        self.visited = []

        self.stack = []
        self.queue = []

        self.reset()
    
    # Resert search
    def reset(self):
        # Containers
        self.stack = []
        self.queue = []
        self.visited = []

        # Vars
        self.current_node = None
        self.result_node = None
        self.search_step_clock = 0
        self.make_path_clock = 0

        # Nodes
        Node.use_a_star_compration = False
        Node.a_start_objective_node = None

        # Cells
        for i in range(MAP_SIZE+1):
            for j in range(MAP_SIZE+1):
                self.cells_matrix[i][j].set_state("none")

        x, y = self.inital_pos
        self.cells_matrix[x][y].set_state("start")
        x, y = self.objetive_pos
        self.cells_matrix[x][y].set_state("objective")
    
    def init_search(self):
        if self.search_algorithm not in SEARCH_ALGORITHMS:
            raise Exception(f"Invalid search {self.search_algorithm}")
        
        self.reset()

        # Vars
        self.search_end = False

        initial_node = Node(self.inital_pos)
        
        if self.search_algorithm == "DFS":
            self.stack.append(initial_node)
        elif self.search_algorithm == "BFS":
            self.queue.append(initial_node)
        elif self.search_algorithm == "UCS":
            heapq.heappush(self.queue, initial_node)
        elif self.search_algorithm == "Greedy":
            self.current_node = initial_node
        elif self.search_algorithm == "A*":
            Node.use_a_star_compration = True
            Node.a_start_objective_node = Node(self.objetive_pos)
            heapq.heappush(self.queue, initial_node)
    
    def abort_search(self):
        self.reset()
        self.search_end = True
    
    def make_path_step(self, dt):
        if self.result_node == None:
            return
        
        if self.make_path_clock < self.make_path_coldown:
            self.make_path_clock += dt
            return
        else:
            self.make_path_clock = 0
        
        if len(self.result_node.path) > 0:
            x, y = self.result_node.path.pop(0)
            self.cells_matrix[x][y].set_state("path")
    
    # Make a step on search
    def step(self, dt):
        if self.search_end:
            self.make_path_step(dt)
            return

        if not self.make_step:
            if not self.search_running:
                return

        self.search_step_clock += dt
        if self.search_step_clock < self.search_step_coldown:
            return
        else:
            self.search_step_clock -= self.search_step_coldown

        if self.search_algorithm == "DFS":
            if len(self.stack) > 0:
                self.current_node = self.stack.pop()
                if self.current_node.pos in self.visited:
                    return
                self.make_step = False

                if self.current_node.pos == self.objetive_pos:
                    self.visited.append(self.current_node)
                    self.result_node = self.current_node
                    self.search_end = True
                    return

                for neighbor in self.current_node.get_neighbors():
                    if not neighbor.pos in self.visited:
                        x, y = neighbor.pos
                        self.cells_matrix[x][y].set_state("generated")
                        self.stack.append(neighbor)

                x, y = self.current_node.pos
                self.cells_matrix[x][y].set_state("visited")
                self.visited.append(self.current_node.pos)
            else:
                self.search_end = True
        elif self.search_algorithm == "BFS":
            if len(self.queue) > 0:
                self.current_node = self.queue.pop(0)
                if self.current_node.pos in self.visited:
                    return
                self.make_step = False

                if self.current_node.pos == self.objetive_pos:
                    self.visited.append(self.current_node)
                    self.result_node = self.current_node
                    self.search_end = True
                    return

                for neighbor in self.current_node.get_neighbors():
                    if not neighbor.pos in self.visited:
                        x, y = neighbor.pos
                        self.cells_matrix[x][y].set_state("generated")
                        self.queue.append(neighbor)

                x, y = self.current_node.pos
                self.cells_matrix[x][y].set_state("visited")
                self.visited.append(self.current_node.pos)
            else:
                
                self.search_end = True
        elif self.search_algorithm == "UCS":
            if len(self.queue) > 0:
                self.current_node = heapq.heappop(self.queue)
                if self.current_node.pos in self.visited:
                    return
                self.make_step = False

                if self.current_node.pos == self.objetive_pos:
                    self.visited.append(self.current_node)
                    self.result_node = self.current_node
                    self.search_end = True
                    return

                for neighbor in self.current_node.get_neighbors():
                    if not neighbor.pos in self.visited:
                        x, y = neighbor.pos
                        self.cells_matrix[x][y].set_state("generated")
                        heapq.heappush(self.queue, neighbor)

                x, y = self.current_node.pos
                self.cells_matrix[x][y].set_state("visited")
                self.visited.append(self.current_node.pos)
            else:
                self.search_end = True

        elif self.search_algorithm == "Greedy":
            if self.current_node.pos == self.objetive_pos:
                self.visited.append(self.current_node)
                self.result_node = self.current_node
                self.search_end = True

            neighbors = sorted(
                self.current_node.get_neighbors(), 
                key=lambda x: x.get_heuristic_value(Node(self.objetive_pos))
            )
            neighbors = list(filter(lambda x: x.pos not in self.visited, neighbors))

            if len(neighbors) == 0:
                self.search_end = True
                return
            
            for neighbor in neighbors:
                x, y = neighbor.pos
                self.cells_matrix[x][y].set_state("generated")

            
            # Set old node as visited
            self.visited.append(self.current_node.pos)
            x, y = self.current_node.pos
            self.cells_matrix[x][y].set_state("visited")

            self.make_step = False
            # Get the node with lower heuristic function cost
            self.current_node = neighbors[0]
        elif self.search_algorithm == "A*":
            if len(self.queue) > 0:
                self.current_node = heapq.heappop(self.queue)

                if self.current_node.pos in self.visited:
                    return
                self.make_step = False

                if self.current_node.pos == self.objetive_pos:
                    self.visited.append(self.current_node)
                    self.result_node = self.current_node
                    self.search_end = True
                    return

                for neighbor in self.current_node.get_neighbors():
                    if not neighbor.pos in self.visited:
                        x, y = neighbor.pos
                        self.cells_matrix[x][y].set_state("generated")
                        heapq.heappush(self.queue, neighbor)

                x, y = self.current_node.pos
                self.cells_matrix[x][y].set_state("visited")
                self.visited.append(self.current_node.pos)
            else:
                
                self.search_end = True

        # Keep start and objective colors
        x, y = self.inital_pos
        self.cells_matrix[x][y].set_state("start")
        x, y = self.objetive_pos
        self.cells_matrix[x][y].set_state("objective")


    
    def update(self, dt):
        self.step(dt)
    