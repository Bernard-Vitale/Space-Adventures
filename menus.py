import pygame


def show_game_over_screen(screen, score, background, restart_button, main_menu_button):
    title_font = pygame.font.Font('fonts/PressStart2P.ttf', 40)
    score_font = pygame.font.Font('fonts/PressStart2P.ttf', 30)

    #Blit Background
    for i in range(0, 2):
        screen.blit(background, (i * background.get_width(), 0 ))

    screen.blit(background, (0, 0))

    # Blit Text
    title_text = title_font.render("Game Over", True, (255, 0, 0))  
    score_text = score_font.render(f'Score: {score}', True, (255, 0, 0))  
    screen.blit(score_text, (screen.get_width() / 2 - score_text.get_width() / 2, screen.get_height() / 2 - score_text.get_height() / 2 + 5))
    screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, screen.get_height() / 2 - title_text.get_height() / 2 - 45))

    # Buttons
    button_surface = pygame.Surface((main_menu_button.get_width() + restart_button.get_width() + 50, main_menu_button.get_height()))
    button_surface.fill((0, 0, 0, 0))
    button_surface.blit(restart_button, (0, 0))
    button_surface.blit(main_menu_button, (button_surface.get_width() - main_menu_button.get_width(), 0))
    screen.blit(button_surface, (screen.get_width() // 2 - button_surface.get_width() // 2, screen.get_height() / 2 - button_surface.get_height() / 2 + 75))

    restart_button_rect = pygame.Rect(
            (screen.get_width() // 2 - button_surface.get_width() // 2,
            screen.get_height() / 2 - button_surface.get_height() / 2 + 75),
            restart_button.get_size()
        )
    main_menu_button_rect = pygame.Rect(
        (screen.get_width() // 2 + button_surface.get_width() // 2 - main_menu_button.get_width(),
        screen.get_height() / 2 - button_surface.get_height() / 2 + 75),
        main_menu_button.get_size()
    )

    pygame.display.flip()

    # Wait for user input to restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return True  # Restart the game
                if main_menu_button_rect.collidepoint(event.pos):
                    return False  # Go to main menu

def show_main_menu(screen, play_button, quit_button, background):
    title_font = pygame.font.Font('fonts/PressStart2P.ttf', 40)
    title_text = title_font.render("Space Adventures", True, (255, 255, 255))  

    # Background code
    for i in range(0, 2):
        screen.blit(background, (i * background.get_width(), 0 ))

    screen.blit(background, (0, 0))

    # Blit Text
    screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, screen.get_height() / 2 - title_text.get_height() / 2 - 50))
    
    # Buttons
    button_surface = pygame.Surface((play_button.get_width() * 2 + 50, play_button.get_height()))
    button_surface.fill((0, 0, 0, 0))
    button_surface.blit(play_button, (0, 0))
    button_surface.blit(quit_button, (button_surface.get_width() - quit_button.get_width(), 0))
    screen.blit(button_surface, (screen.get_width() // 2 - button_surface.get_width() // 2, screen.get_height() / 2 - button_surface.get_height() / 2 + 50))

    play_button_rect = pygame.Rect(
            (screen.get_width() // 2 - button_surface.get_width() // 2,
            screen.get_height() / 2 - button_surface.get_height() / 2 + 50),
            play_button.get_size()
        )
    quit_button_rect = pygame.Rect(
        (screen.get_width() // 2 + button_surface.get_width() // 2 - quit_button.get_width(),
        screen.get_height() / 2 - button_surface.get_height() / 2 + 50),
        quit_button.get_size()
    )

    pygame.display.flip()

    # Wait for user input to play or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return True  # Start the game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    return False  # Quit the game

def show_paused_screen(screen, resume_button, quit_button):
    paused_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    # Set the transparency
    paused_surface.set_alpha(100)
    paused_surface.fill((0, 0, 0,))
    screen.blit(paused_surface, (0, 0))

    # Blit Text
    title_font = pygame.font.Font('fonts/PressStart2P.ttf', 30)
    instruction_font = pygame.font.Font('fonts/PressStart2P.ttf', 15)
    title_text = title_font.render("Paused", True, (255, 255, 255))  
    screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, screen.get_height() / 2 - title_text.get_height() / 2 - 50))

    # Buttons
    button_surface = pygame.Surface((resume_button.get_width() + quit_button.get_width() + 50, resume_button.get_height()))
    button_surface.fill((0, 0, 0, 0))
    button_surface.blit(resume_button, (0, 0))
    button_surface.blit(quit_button, (button_surface.get_width() - quit_button.get_width(), 0))
    screen.blit(button_surface, (screen.get_width() // 2 - button_surface.get_width() // 2, screen.get_height() / 2 - button_surface.get_height() / 2 + 35))

    pygame.display.flip()

    resume_button_rect = pygame.Rect(
            (screen.get_width() // 2 - button_surface.get_width() // 2,
            screen.get_height() / 2 - button_surface.get_height() / 2 + 35),
            resume_button.get_size()
        )
    quit_button_rect = pygame.Rect(
        (screen.get_width() // 2 + button_surface.get_width() // 2 - quit_button.get_width(),
        screen.get_height() / 2 - button_surface.get_height() / 2 + 35),
        quit_button.get_size()
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button_rect.collidepoint(event.pos):
                    return True  # Start the game
                if quit_button_rect.collidepoint(event.pos):
                    return False  # Quit the game

    





