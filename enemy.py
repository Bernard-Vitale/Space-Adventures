import pygame
from laser import Laser

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, laser):
        super().__init__()
        self.speed = 400
        self.last_shot_time = 100  # initial shot time for nearly instant first shot
        self.shot_cooldown = 500
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))  
        self.mask = pygame.mask.from_surface(self.image)
        self.laser = laser
        self.laser_sound = pygame.mixer.Sound('sounds/enemy_laser.mp3')
        self.laser_sound.set_volume(0.3)

    def update(self, delta_time, player, enemy_laser_group):
        self.rect.y += self.speed * delta_time 

        if player.x - 20 < self.rect.x < player.x + 20:
            self.shoot(enemy_laser_group)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft) 

    def shoot(self, enemy_laser_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shot_cooldown:
            laser = Laser(self.rect.centerx - 5, self.rect.bottom, self.laser, 1000)
            enemy_laser_group.add(laser)
            self.laser_sound.play()
            self.last_shot_time = current_time
