from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.camera_offset = pygame.Vector2(0, 0)
    
    def camera_movement(self):
        dx, dy = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[0]:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
            self.camera_offset.x += dx
            self.camera_offset.y += dy
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def scale_cells(self, factor):
        cells = [x for x in self if x.type == "cell"]
        for cell in cells:
            cell.scale_by(factor)

    def update(self, *args, **kwargs):
        self.camera_movement()
        return super().update(*args, **kwargs)

    def draw(self, surface):
        for sprite in self:
            surface.blit(sprite.image, sprite.rect.topleft + self.camera_offset)
