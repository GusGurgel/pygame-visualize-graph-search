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
                    self.grid.stop_search()

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