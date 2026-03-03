import codecs

with codecs.open('main.py', 'r', 'utf-8') as f:
    content = f.read()

# 1. Add RESIZABLE and logical_screen
content = content.replace(
    'screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))',
    'screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)\nlogical_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))'
)

# 2. Add global screen in run_menu and main
content = content.replace(
    'def run_menu():',
    'def run_menu():\n    global screen'
)
content = content.replace(
    'def main():',
    'def main():\n    global screen'
)

# 3. Global replacements for drawing
content = content.replace('screen.fill', 'logical_screen.fill')
content = content.replace('screen.blit', 'logical_screen.blit')
content = content.replace('draw_text(screen,', 'draw_text(logical_screen,')
content = content.replace('draw_text_center(screen,', 'draw_text_center(logical_screen,')

# 4. Add VIDEORESIZE to run_menu
menu_event = """            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)"""
content = content.replace('            if event.type == pygame.QUIT:\n                pygame.quit()\n                sys.exit()', menu_event, 1)

# 5. Add VIDEORESIZE to main loop
main_event = """                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)"""
content = content.replace('                if event.type == pygame.QUIT:\n                    pygame.quit()\n                    sys.exit()', main_event, 1)

# 6. Modify display flip in run_menu
run_menu_flip = """        scaled_screen = pygame.transform.scale(logical_screen, screen.get_size())
        screen.blit(scaled_screen, (0, 0))
        pygame.display.flip()"""
content = content.replace('        pygame.display.flip()\n        clock.tick(FPS)', run_menu_flip + '\n        clock.tick(FPS)', 1)

# 7. Modify display flip in main (pause menu)
pause_flip = """                scaled_screen = pygame.transform.scale(logical_screen, screen.get_size())
                screen.blit(scaled_screen, (0, 0))
                pygame.display.flip()"""
content = content.replace('                pygame.display.flip()\n                clock.tick(FPS)\n                continue', pause_flip + '\n                clock.tick(FPS)\n                continue', 1)

# 8. Modify display flip in main (game loop end)
game_flip = """            scaled_screen = pygame.transform.scale(logical_screen, screen.get_size())
            screen.blit(scaled_screen, (0, 0))
            pygame.display.flip()"""
content = content.replace('            pygame.display.flip()\n            clock.tick(FPS)\n\n    pygame.quit()', game_flip + '\n            clock.tick(FPS)\n\n    pygame.quit()', 1)

with codecs.open('main.py', 'w', 'utf-8') as f:
    f.write(content)

print("main.py modified for resizing.")
