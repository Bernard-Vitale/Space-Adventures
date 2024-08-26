import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, laser):
        super().__init__()
        self.speed = 600  # Speed in pixels per second
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.laser = laser

    def move(self, delta_time, keys, border):
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > border + 8:
            self.rect.x -= self.speed * delta_time
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < (1280 - 8 - border):
            self.rect.x += self.speed * delta_time

        # Ensure the player stays within screen bounds
        self.rect.x = max(0, min(self.rect.x, pygame.display.get_surface().get_width() - self.rect.width))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def shoot(self, lasers):
        laser = Laser(self.rect.centerx - 5, self.rect.top, self.laser, 750)
        lasers.add(laser)