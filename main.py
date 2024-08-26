import pygame
import random
import math

import pygame.locals
from laser import Laser
from meteor import Meteor
from player import Player
from enemy import Enemy
from menus import show_game_over_screen, show_main_menu, show_paused_screen

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Game:
    def __init__(self):
        pygame.init()

        #Sprite Groups
        self.lasers = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Buttons 
        self.play_button = pygame.image.load('images/playButton.png') 
        self.play_button = pygame.transform.scale(self.play_button, (200, 70))
        self.quit_button = pygame.image.load('images/quitButton.png')
        self.quit_button = pygame.transform.scale(self.quit_button, (200, 70))
        self.restart_button = pygame.image.load('images/restartButton.png') 
        self.restart_button = pygame.transform.scale(self.restart_button, (200, 70))
        self.main_menu_button = pygame.image.load('images/mainMenuButton.png')
        self.main_menu_button = pygame.transform.scale(self.main_menu_button, (200, 70))
        self.resume_button = pygame.image.load('images/resumeButton.png')
        self.resume_button = pygame.transform.scale(self.resume_button, (200, 70))

        pygame.display.set_caption('Space Adventures')
        self.font = pygame.font.Font('fonts/PressStart2P.ttf', 20)
        self.breakdown_title_font = pygame.font.Font('fonts/PressStart2P.ttf', 20)
        self.totalsFont = pygame.font.Font('fonts/PressStart2P.ttf', 30)
        self.breakdown_title = self.breakdown_title_font.render("Totals:", True, (255, 255, 244))

        # Images
        self.heart_image = pygame.image.load('images/heart.png')
        self.heart_image = pygame.transform.scale(self.heart_image, (int(45), int(38)))
        self.player_image = pygame.image.load('images/player.png')
        self.player_image = pygame.transform.scale(self.player_image, (int(50), int(70)))
        self.enemy_starship = pygame.image.load('images/enemyStarship.png') 
        self.enemy_starship = pygame.transform.scale(self.enemy_starship, (50, 70))
        self.enemy_meteor = pygame.image.load('images/meteor.png')
        self.enemy_meteor = pygame.transform.scale(self.enemy_meteor, (50, 70))
        self.player_laser = pygame.image.load('images/player_laser.png')
        self.player_laser = pygame.transform.scale(self.player_laser, (int(10), int(25)))
        self.enemy_laser = pygame.image.load('images/enemy_laser.png')
        self.enemy_laser = pygame.transform.scale(self.enemy_laser, (int(10), int(25)))

        # Window Icon
        pygame.display.set_icon(self.enemy_meteor)

        # Background Variables
        self.background_image = pygame.image.load('images/background.png')
        self.background_image = pygame.transform.scale(self.background_image, (int(SCREEN_WIDTH-600), int(SCREEN_HEIGHT)))
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_surface.blit(self.background_image, (300, 0))

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #, pygame.RESIZABLE)
        # self.screen =pygame.display.set_mode((0, 0), pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.player = Player(self.screen.get_width() / 2 - 45, self.screen.get_height() - 90, self.player_image, self.player_laser)
        self.player_score = 0
        self.player_lives = 3
        self.border_width = 300
        self.enemies_destroyed = 0
        self.meteors_destroyed = 0
        self.lasers.empty()
        self.enemy_lasers.empty()
        self.meteors.empty()
        self.enemies.empty()
        self.last_meteor_spawn_time = pygame.time.get_ticks()
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.running = True
        self.game_over = False
        self.meteor_speed = 350
        self.paused = False

    def spawn_meteor(self):
        # Pick random x cord to spawn
        meteor_x = random.randint(self.border_width, self.screen.get_width() - 70 - self.border_width)
        meteor = Meteor(meteor_x, 0, self.meteor_speed, self.enemy_meteor)
        self.meteors.add(meteor)
        self.last_meteor_spawn_time = pygame.time.get_ticks()

    def spawn_enemy(self):
        # Pick random x cord to spawn
        enemy_x = random.randint(self.border_width, self.screen.get_width() - 70 - self.border_width)
        enemy = Enemy(enemy_x, 0, self.enemy_starship, self.enemy_laser)
        self.enemies.add(enemy)
        self.last_enemy_spawn_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pygame.K_SPACE and not self.paused:
                    self.player.shoot(self.lasers)

    def remove_off_screen_sprites(self):
        # Remove off-screen meteors
        for meteor in self.meteors:
            if meteor.rect.bottom > self.screen.get_height():
                meteor.kill()

        # Remove off-screen enemy lasers
        for enemy_laser in self.enemy_lasers:
            if enemy_laser.rect.top < 0:
                enemy_laser.kill()

        # Remove off-screen lasers
        for laser in self.lasers:
            if laser.rect.bottom < 0:
                laser.kill()

        # Remove off-screen enemies
        for enemy in self.enemies:
            if enemy.rect.bottom > self.screen.get_height():
                enemy.kill()
            
    def check_collisions(self):
        # Check laser and meteor collisions
        for laser in self.lasers:
            for meteor in self.meteors:
                if pygame.sprite.collide_rect(laser, meteor):
                    laser.kill()
                    meteor.kill()
                    self.player_score += 1
                    self.meteors_destroyed += 1
                    break

            # Check laser and enemy collisions
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(laser, enemy):
                    laser.kill()
                    enemy.kill()
                    self.player_score += 2
                    self.enemies_destroyed += 1
                    break

            # Check collisions with enemy lasers
            for enemy_laser in self.enemy_lasers:
                enemy_laser_rect = enemy_laser.rect
                if pygame.sprite.collide_rect(laser, enemy_laser):
                    laser.kill()
                    enemy_laser.kill()
                    break


        # Check enemy laser and player collisions
        for enemy_laser in self.enemy_lasers:
            if pygame.sprite.collide_rect(self.player, enemy_laser):
                self.player_lives -= 1
                enemy_laser.kill()
                if self.player_lives == 0:
                    self.running = False
                    self.game_over = True
                    break

        # Check meteor and player collisions
        for meteor in self.meteors:
            if pygame.sprite.collide_rect(self.player, meteor):
                # Offset is used for perfect Pixel Collsion, Refer to the Pygame documentation for explanation 
                # https://www.pygame.org/docs/ref/mask.html
                offset = (self.player.rect.left - meteor.rect.left, self.player.rect.top - meteor.rect.top)
                if self.player.mask.overlap(meteor.mask, offset):
                    self.player_lives -= 1
                    meteor.kill()
                    if self.player_lives == 0:
                        self.running = False
                        self.game_over = True
                        break

        # Check enemy and player collisions
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                offset = (self.player.rect.left - enemy.rect.left, self.player.rect.top - enemy.rect.top)
                if self.player.mask.overlap(enemy.mask, offset):
                    self.player_lives -= 1
                    enemy.kill()
                    if self.player_lives == 0:
                        self.running = False
                        self.game_over = True
                        break

    def update_sprites(self, delta_time):
        self.lasers.update(delta_time, False)
        self.enemy_lasers.update(delta_time, True)
        self.meteors.update(delta_time)
        self.enemies.update(delta_time, self.player.rect, self.enemy_lasers)

        # Check collisions using groups
        self.check_collisions()

    def draw(self):
        self.screen.fill((20, 20, 20))
        self.screen.blit(self.background_surface, (0, 0))

        # LEFT BORDER
        pygame.draw.rect(self.screen, (10, 10, 10), (0, 0, self.border_width, SCREEN_HEIGHT))
        score_text = self.font.render(f'Score: {self.player_score}', True, (255, 255, 255))
        score_text_x = (self.border_width / 2) - (score_text.get_width() / 2)
        score__text_y = (self.screen.get_height() / 2 - score_text.get_height() / 2)
        self.screen.blit(score_text, (score_text_x, score__text_y))

        lives_text = self.font.render("Lives:", True, (255, 255, 255))
        heart_image = self.heart_image
        lives_surface = pygame.Surface((self.border_width, heart_image.get_height()+10))
        lives_surface.fill((10, 10, 10))
        lives_text_x = 10
        lives_text_y = (lives_surface.get_height()/2 - lives_text.get_height()/2)
        lives_surface.blit(lives_text, (lives_text_x, lives_text_y))

        heart_image_x = (10 + lives_text.get_width())
        heart_image_y = (lives_surface.get_height()/2 - heart_image.get_height()/2)
        for i in range(self.player_lives):
            if i != 0:
                heart_image_x += (heart_image.get_width() + 10)

            lives_surface.blit(heart_image, (heart_image_x, heart_image_y))

        lives_surface_x = (self.border_width/2 - lives_surface.get_width()/2)
        lives_surface_y = (self.screen.get_height() - lives_surface.get_height() - 10)
        self.screen.blit(lives_surface, (lives_surface_x, lives_surface_y))
            

        self.player.draw(self.screen)
        self.lasers.draw(self.screen)
        self.enemy_lasers.draw(self.screen)
        self.meteors.draw(self.screen)
        self.enemies.draw(self.screen)

        # RIGHT BORDER
        pygame.draw.rect(self.screen, (10, 10, 10),  (SCREEN_WIDTH - self.border_width, 0, self.border_width, SCREEN_HEIGHT))

        # All the parts in the breakdown section
        breakdown_title = self.breakdown_title

        enemy_image = self.enemy_starship
        enemies_total = self.totalsFont.render(f' x {self.enemies_destroyed}', True, (255, 255, 255))

        meteor_image = self.enemy_meteor
        meteors_total = self.totalsFont.render(f' x {self.meteors_destroyed}', True, (255, 255, 255))

        # This height is a sum of all the pixels that will be in it. The reason it is written complicated because it is a combination of 
        # of the three variables below (breakdown_title_y + enemy_image_y + meteor_image_y)
        breakdown_height = ((breakdown_title.get_height()*3 + enemy_image.get_height() + 70 + meteor_image.get_height()))
        breakdown_surface = pygame.Surface((self.border_width, breakdown_height))
        breakdown_surface.fill((10, 10, 10))

        combined_image_count_width = enemy_image.get_width() + enemies_total.get_width()

        breakdown_title_x = ((breakdown_surface.get_width() - breakdown_title.get_width() ) / 2)
        breakdown_title_y = breakdown_title.get_height()
        # Position the enemy image and the enemies total text on the breakdown surface
        enemy_image_x = (breakdown_surface.get_width() - combined_image_count_width) / 2
        enemy_image_y = breakdown_title_y + 35 + breakdown_title_y # The 35 is for some spacing

        enemies_total_x = enemy_image_x + enemy_image.get_width()
        enemies_total_y = enemy_image_y + (enemy_image.get_height() - enemies_total.get_height()) / 2



        # Position the Meteor image and the enemies total text on the breakdown surface
        meteor_image_x = (breakdown_surface.get_width() - combined_image_count_width) / 2
        meteor_image_y = enemy_image.get_height() + enemy_image_y + 35 # the 35 is for some padding

        meteors_total_x = meteor_image_x + meteor_image.get_width()
        meteors_total_y = meteor_image_y + (meteor_image.get_height() - meteors_total.get_height()) / 2

        # Blit the breakdown surface to the screen at the right border
        breakdown_surface.blit(breakdown_title, (breakdown_title_x, breakdown_title_y))
        breakdown_surface.blit(enemy_image, ((breakdown_surface.get_width() - combined_image_count_width) / 2, enemy_image_y))
        breakdown_surface.blit(enemies_total, (enemies_total_x, enemies_total_y))
        breakdown_surface.blit(meteor_image, ((breakdown_surface.get_width() - combined_image_count_width) / 2, meteor_image_y))
        breakdown_surface.blit(meteors_total, (meteors_total_x, meteors_total_y))

        self.screen.blit(breakdown_surface, (SCREEN_WIDTH - self.border_width, (SCREEN_HEIGHT - breakdown_surface.get_height())/2, self.border_width, SCREEN_HEIGHT))



    def run(self):
        last_time = pygame.time.get_ticks()
        self.last_meteor_spawn_time = pygame.time.get_ticks()
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        while self.running:
            self.handle_events()

            if not self.paused:
                current_time = pygame.time.get_ticks()
                delta_time = (current_time - last_time) / 1000
                last_time = current_time

                # Update player position and handle key presses
                keys = pygame.key.get_pressed()
                self.player.move(delta_time, keys, self.border_width)

                # Handle Spawning Enemies depending on their last spawn
                if current_time - self.last_meteor_spawn_time > 2000:
                    self.spawn_meteor()
                if current_time - self.last_enemy_spawn_time > 5000:
                    self.spawn_enemy()

                # Update all the enemies and lasers positions and check for collisions
                self.update_sprites(delta_time)

                # Handle game over logic
                if self.game_over:
                    self.running = False
                    if show_game_over_screen(self.screen, self.player_score, self.background_image, self.restart_button, self.main_menu_button):
                        self.reset_game()
                    else:
                        if show_main_menu(self.screen, self.play_button, self.quit_button, self.background_image):
                            self.reset_game()
                        else:
                            pygame.quit()
                            return

                # Draw the frame
                self.draw()

            else:
                # Handle the pause menu
                pause_start_time = pygame.time.get_ticks()
                if show_paused_screen(self.screen, self.resume_button, self.quit_button):
                    self.paused = False
                    # Adjust last_time to prevent time jump
                    last_time += pygame.time.get_ticks() - pause_start_time
                else:
                    self.running = False
                    if show_main_menu(self.screen, self.play_button, self.quit_button, self.background_image):
                        self.reset_game()
                    else:
                        pygame.quit()
                        return

            # Flip the display after all drawing is done
            pygame.display.flip()

            # Limit the frame rate
            self.clock.tick(60)

        pygame.quit()
        return

if __name__ == "__main__":
    game_instance = Game()
    if show_main_menu(game_instance.screen, game_instance.play_button, game_instance.quit_button, game_instance.background_image):
        game_instance.run()
    else:
        pygame.quit()

