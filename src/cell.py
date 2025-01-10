from settings import *

class Cell(pygame.sprite.Sprite):
    def __init__(self, matrix_pos=(0, 0), *groups):
        super().__init__(*groups)

        self.display_rect = pygame.display.get_surface().get_frect()

        self.state = "none"
        self.type = "cell"
        self.matrix_pos = matrix_pos

        self.image = pygame.surface.Surface(
            (CELL_SIZE, CELL_SIZE),
            pygame.SRCALPHA
        )

        self.rect = self.image.get_frect()

        self.rect.bottomleft = self.display_rect.bottomleft + pygame.Vector2(
             (CELL_SIZE * self.matrix_pos[0]),
            -(CELL_SIZE * self.matrix_pos[1]),
        )

        self.set_state(state="none")

    def set_state(self, state=None):
        if state == None:
            state = self.state

        if state not in CELL_STATES:
            raise Exception(f"Invalide cell state: {state}")
        
        self.state = state

        self.image.fill(pygame.SRCALPHA)

        pygame.draw.rect(
            self.image, 
            COLORS["cell_" + state],
            pygame.Rect((0, 0), (CELL_SIZE, CELL_SIZE)),
        )
        
        pygame.draw.rect(
            self.image, 
            COLORS["cell_stroke"],
            pygame.Rect((0, 0), (CELL_SIZE, CELL_SIZE)),
            CELL_STROKE_SIZE
        )

        text = CELL_FONT.render(f"{self.matrix_pos[0]},{self.matrix_pos[1]}", True, COLORS["text_" + state])
        text_rect = text.get_frect(center=(CELL_SIZE/2, CELL_SIZE/2))
        self.image.blit(text, text_rect)