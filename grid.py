from settings import *
from queue import PriorityQueue
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
    
        self.search_running = False
        self.search_algorithm = "BFS"

        self.inital_pos = (0, 0)
        self.objetive_pos = (5, 5)
        self.current_node = None
        self.result_node = None
        self.visited = []

        self.stack = []
        self.queue = []
        self.priority_queue = PriorityQueue()

        self.reset()
        self.init_search()
    
    # Resert search
    def reset(self):
        # Containers
        self.stack = []
        self.queue = []
        self.visited = []
        self.priority_queue = PriorityQueue()

        # Vars
        self.current_node = None
        self.result_node = None
        self.search_step_clock = 0

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
        self.search_running = True

        initial_node = Node(self.inital_pos)
        
        if self.search_algorithm == "DFS":
            self.stack.append(initial_node)
        elif self.search_algorithm == "BFS":
            self.queue.append(initial_node)
    
    def stop_search(self):
        self.reset()
        self.search_running = False
    
    # Make a step on search
    def step(self, dt):
        if not self.search_running:
            return

        self.search_step_clock += dt
        if self.search_step_clock < self.search_step_coldown:
            return
        else:
            self.search_step_clock = 0

        if self.search_algorithm == "DFS":
            if len(self.stack) > 0:
                self.current_node = self.stack.pop()
                if self.current_node.pos in self.visited:
                    return

                if self.current_node.pos == self.objetive_pos:
                    self.visited.append(self.current_node)
                    self.result_node = self.current_node
                    self.search_running = False
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
                self.search_running = False
        elif self.search_algorithm == "BFS":
            if len(self.queue) > 0:
                self.current_node = self.queue.pop(0)
                if self.current_node.pos in self.visited:
                    return

                if self.current_node.pos == self.objetive_pos:
                    self.visited.append(self.current_node)
                    self.result_node = self.current_node
                    self.search_running = False
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
                self.search_running = False

        # Keep start and objective colors
        x, y = self.inital_pos
        self.cells_matrix[x][y].set_state("start")
        x, y = self.objetive_pos
        self.cells_matrix[x][y].set_state("objective")

    
    def update(self, dt):
        self.step(dt)
    