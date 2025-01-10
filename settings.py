import pygame
import pygame_gui
import ctypes
from os.path import join
from platform import system

# [ APP ]
WINDOW_WIDTH, WINDOW_HEIGHT = (1200, 800)
WINDOW_TITLE = "Interative Search"
RELATIVE_PATH = join(".", "source", "interactive")

# [ SEARCH ]
SEARCH_ALGORITHMS = ["DFS", "BFS", "UCS", "Greedy", "A*"]
SEARCH_STEP_COLDOWN = 1

MAP_SIZE = 30  # cols x rows

F1 = lambda pos: (pos[0] - 1, pos[1])
F2 = lambda pos: (pos[0] + 1, pos[1])
F3 = lambda pos: (pos[0], pos[1] - 1)
F4 = lambda pos: (pos[0], pos[1] + 1)

ACTIONS = [F1, F2, F3, F4]

# [ CELL ]
START_CELL_STEP_COLDOWN = 0.05
CELL_SCALE_FACTOR = 0.1
CELL_SCALE_COLDOWN = 0.05
pygame.font.init()
CELL_FONT = pygame.font.Font(None, 13)
CELL_STATES = ["none", "generated", "visited", "objective", "start"]
CELL_SIZE = WINDOW_HEIGHT/(MAP_SIZE+1)
CELL_STROKE_SIZE = 1
CELL_SCALE_MAX = 5
CELL_SCALE_MIN = 1

# [ COLORS ]
COLORS = {
    "cell_none": "#d9eafd",
    "cell_generated": "#4da1a9",
    "cell_visited": "#2e5077",
    "cell_objective": "#28a745",
    "cell_start": "#ffc107",
    "cell_stroke": "black",

    "bg": "#bcccdc",
    "text_none": "black",
    "text_generated": "white",
    "text_visited": "white",
    "text_start": "black",
    "text_objective": "white",
}