import pygame

class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        super().__init__()
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y)) 
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.rect.y += self.speed * delta_time

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft) 
    
