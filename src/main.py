from settings import *
from groups import *
from grid import *

class App:
    def __init__(self):
        # Window size fix
        if system() == "Windows":
            ctypes.windll.user32.SetProcessDPIAware()

        # Init services
        pygame.init()

        # Creating main surface
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1
        )
        self.dispaly_rect = self.display_surface.get_frect()
        self.sub_display_surface = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Set title
        pygame.display.set_caption(WINDOW_TITLE)

        # Proprieties
        self.running = True
        self.clock = pygame.Clock()
        self.all_sprites = AllSprites()

        self.grid = Grid(self.all_sprites)

        # Setting up ui
        self.ui_manager = pygame_gui.UIManager(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            theme_path=join(RELATIVE_PATH, "ui_theme.json"),
        )
        
        self.sub_display_scale = 1

        # Scale timer
        self.scaled = False
        self.scale_clock = 0
        self.scale_coldown = CELL_SCALE_COLDOWN

        db = self.dispaly_rect.bottom
        dr = self.dispaly_rect.right

        start_button_rect = pygame.Rect((dr-295,db-100), (100, 50))

        reset_button_rect = start_button_rect.copy()
        reset_button_rect.topleft += pygame.Vector2(start_button_rect.width+10, 0)

        step_button_rect = pygame.Rect(
            (start_button_rect.x, start_button_rect.y - start_button_rect.h - 10),
            (start_button_rect.w*2+10, start_button_rect.h)

        )

        algorithm_list_rect = step_button_rect.copy()
        algorithm_list_rect.h -= 20
        algorithm_list_rect.y -= step_button_rect.h - 10
        
        cost_function_list_rect = algorithm_list_rect.copy()
        cost_function_list_rect.y -= algorithm_list_rect.h + 10
        
        heuristic_function_list_rect = cost_function_list_rect.copy()
        heuristic_function_list_rect.y -= algorithm_list_rect.h + 10

        self.start_button = pygame_gui.elements.UIButton(
            start_button_rect,
            "start",
            self.ui_manager,
        )

        self.pause_button = pygame_gui.elements.UIButton(
            reset_button_rect,
            "continue",
            self.ui_manager,
        )
        
        self.step_button = pygame_gui.elements.UIButton(
            step_button_rect,
            "step",
            self.ui_manager,
        )

        self.algorithm_list = pygame_gui.elements.UIDropDownMenu(
            SEARCH_ALGORITHMS,
            SEARCH_ALGORITHMS[0],
            algorithm_list_rect,
            self.ui_manager
        )

        self.cost_function_list = pygame_gui.elements.UIDropDownMenu(
            NODE_COST_FUNCTIONS,
            NODE_COST_FUNCTIONS[0],
            cost_function_list_rect,
            self.ui_manager
        )
        
        self.heuristic_function_list = pygame_gui.elements.UIDropDownMenu(
            NODE_HEURISTIC_FUNCTIONS,
            NODE_HEURISTIC_FUNCTIONS[0],
            heuristic_function_list_rect,
            self.ui_manager
        )

    def handle_scale_coldown(self, dt):
        if not self.scaled:
            return
        
        self.scale_clock += dt
        if self.scale_clock >= self.scale_coldown:
            self.scale_clock = 0
            self.scaled = False
    
    def sum_scale_grid(self, scale):
        if not self.scaled:
            self.scaled = True
            self.sub_display_scale += scale
            if self.sub_display_scale >= CELL_SCALE_MAX:
                self.sub_display_scale = CELL_SCALE_MAX
            if self.sub_display_scale < CELL_SCALE_MIN:
                self.sub_display_scale = CELL_SCALE_MIN
    
    def handle_button_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                if self.grid.search_end:
                    self.grid.init_search()
                else:
                    self.grid.abort_search()
                self.start_button.set_text(
                    "start" if self.grid.search_end else "abord"
                ) 
            elif event.ui_element == self.pause_button:
                self.grid.search_running = not self.grid.search_running
                self.pause_button.set_text(
                    "pause" if self.grid.search_running else "continue"
                )
            elif event.ui_element == self.step_button:
                self.grid.make_step = True
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.algorithm_list:
                self.grid.search_algorithm = self.algorithm_list.selected_option[0]
            elif event.ui_element == self.cost_function_list:
                Node.cost_function = self.cost_function_list.selected_option[0]
            elif event.ui_element == self.heuristic_function_list:
                Node.heuristic_function = self.heuristic_function_list.selected_option[0]
            
            self.start_button.set_text("start")
            self.grid.abort_search()


    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.running = False
                if event.type == pygame.MOUSEWHEEL:
                    if event.y != 0:
                        self.sum_scale_grid(event.y*CELL_SCALE_FACTOR)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.grid.init_search()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.grid.abort_search()
                
                self.ui_manager.process_events(event)
                self.handle_button_events(event)

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_UP] or keys[pygame.K_DOWN]) and not self.scaled:
                scale_factor = keys[pygame.K_UP] - keys[pygame.K_DOWN]
                scale_factor *= CELL_SCALE_FACTOR

                self.sum_scale_grid(scale_factor)

            self.ui_manager.update(dt)
            self.all_sprites.update(dt)
            self.grid.update(dt)
            self.handle_scale_coldown(dt)

            self.display_surface.fill(COLORS["bg"])
            self.sub_display_surface.fill(COLORS["bg"])
            self.all_sprites.draw(self.sub_display_surface)
            self.display_surface.blit(
                pygame.transform.smoothscale_by(
                    self.sub_display_surface, 
                    (self.sub_display_scale, self.sub_display_scale)
                )
            )

            self.ui_manager.draw_ui(self.display_surface)

            # flip the screen buffer
            pygame.display.update()

        # Quit services
        pygame.quit()

if __name__ == "__main__":
    app = App()
    app.run()