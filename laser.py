import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, image, bullet_speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = bullet_speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time, enemy_bullet=False):
        if enemy_bullet:
            self.rect.y += self.speed * delta_time
        else:
            self.rect.y -= self.speed * delta_time

        # Remove the laser if it goes off-screen
        if self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)