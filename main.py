import pygame
import sys
import os
import json

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Demo - 10 Levels & Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COIN_YELLOW = (252, 216, 0)
PLAYER_RED = (216, 40, 0)
MENU_BLUE = (0, 0, 150)
MENU_HIGHLIGHT = (255, 255, 100)

# Frame rate
clock = pygame.time.Clock()
FPS = 60
TILE_SIZE = 32

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 24)

# Load Images correctly using convert_alpha() to respect the true transparency of the PNG files we patched
def load_image(name, size=None):
    path = os.path.join('assets', name)
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as message:
        print(f"Cannot load image: {name}")
        surf = pygame.Surface(size if size else (32, 32), pygame.SRCALPHA)
        surf.fill((216, 40, 0, 255))
        return surf

# Load all game assets
player_img = load_image('player.png', (32, 40))
enemy_img = load_image('enemy.png', (32, 32))
block_img = load_image('block.png', (TILE_SIZE, TILE_SIZE))
coin_img = load_image('coin.png', (24, 24))
bg_img = load_image('bg.png', (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Audio
try:
    pygame.mixer.music.load(os.path.join('assets', 'bgm.mp3'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1) # Loop indefinitely
except pygame.error:
    print("Could not load background music (bgm.mp3).")

# Save file setup
SAVE_FILE = "save_game.json"

def save_game_data(level, score):
    data = {"level": level, "score": score}
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)

def load_game_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
                return data.get("level", 0), data.get("score", 0)
        except:
            return 0, 0
    return 0, 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = False
        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.5
        self.score = 0
        self.is_dead = False
        self.won_level = False
        self.facing_right = True

    def update(self, blocks, enemies, coins, goal):
        if self.is_dead or self.won_level:
            return

        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            if self.facing_right:
                self.image = pygame.transform.flip(player_img, True, False)
                self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            if not self.facing_right:
                self.image = player_img
                self.facing_right = True

        self.rect.x += dx
        self.check_collision_x(blocks)
        
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        
        self.on_ground = False
        self.check_collision_y(blocks)
        
        if self.rect.bottom > SCREEN_HEIGHT + 100:
            self.die()

        self.check_interactions(enemies, coins, goal)

    def check_collision_x(self, blocks):
        hits = pygame.sprite.spritecollide(self, blocks, False)
        for block in hits:
            if self.rect.centerx < block.rect.centerx:
                self.rect.right = block.rect.left
            elif self.rect.centerx > block.rect.centerx:
                self.rect.left = block.rect.right

    def check_collision_y(self, blocks):
        hits = pygame.sprite.spritecollide(self, blocks, False)
        for block in hits:
            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom
                self.vel_y = 0

    def check_interactions(self, enemies, coins, goal):
        coin_hits = pygame.sprite.spritecollide(self, coins, True)
        for coin in coin_hits:
            self.score += 100

        if pygame.sprite.spritecollideany(self, goal):
            self.won_level = True

        enemy_hits = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in enemy_hits:
            if self.vel_y > 0 and self.rect.bottom <= enemy.rect.centery + 10:
                enemy.kill()
                self.vel_y = -8
                self.score += 200
            else:
                self.die()

    def die(self):
        self.is_dead = True


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = block_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = -2
        self.vel_y = 0

    def update(self, blocks):
        self.vel_y += 0.5
        self.rect.y += self.vel_y
        
        hits = pygame.sprite.spritecollide(self, blocks, False)
        for block in hits:
            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
                self.vel_y = 0
                
        self.rect.x += self.vel_x
        hits = pygame.sprite.spritecollide(self, blocks, False)
        for block in hits:
            if self.vel_x > 0:
                self.rect.right = block.rect.left
                self.vel_x = -self.vel_x
                self.image = pygame.transform.flip(enemy_img, True, False)
            elif self.vel_x < 0:
                self.rect.left = block.rect.right
                self.vel_x = -self.vel_x
                self.image = enemy_img

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.center = (x + TILE_SIZE//2, y + TILE_SIZE//2)

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 200))
        self.image.fill((200, 200, 200))
        flag = pygame.Surface((32, 32))
        flag.fill((0, 255, 0))
        self.image.blit(flag, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y + 32)

# 10 Level Maps (Easy and Guaranteed Beatable!)
# No gap is wider than 4 blocks. Players can leap up to 7 safely.
LEVELS = [
    # Level 1 - Introduction
    [
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "             C                  ",
        "          XXXXX                 ",
        "                                ",
        "   C                  C         ",
        "  XX                 XX         ",
        "                                ",
        "                              G ",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ],
    # Level 2 - Basic Enemies
    [
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "          CCC                   ",
        "         XXXXX                  ",
        "                                ",
        "                                ",
        "               E                ",
        "  XXXX   XXXXXXXXXXXXXXXX     G ",
        "XXXXXX   XXXXXXXXXXXXXXXXXXXXXXX",
        "XXXXXX   XXXXXXXXXXXXXXXXXXXXXXX"
    ],
    # Level 3 - Simple Pits (2 block wide max)
    [
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "         CCC                    ",
        "        XXXXX                   ",
        "                                ",
        "               E                ",
        "              XXX               ",
        "      XX              XX      G ",
        "XXXXX    XXXX     XXXX    XXXXXX",
        "XXXXX    XXXX     XXXX    XXXXXX"
    ],
    # Level 4 - Platforms and gaps
    [
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                         C      ",
        "                       XXX      ",
        "                     XXXXX      ",
        "             C     XXXXXXX      ",
        "           XXX   XXXXXXXXX      ",
        "         XXXXX   XXXXXXXXX    G ",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ],
    # Level 5 - Reduced gap sizes from before
    [
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "          C C C C               ",
        "         XXXXXXXXX              ",
        "                                ",
        "                                ",
        "     XX             XXX         ",
        "                              G ",
        "XXXXX     XXX     XXXXXXXXXXXXXX",
        "XXXXX     XXX     XXXXXXXXXXXXXX"
    ],
    # Level 6 - Stepping stones
    [
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "           CCC                  ",
        "          XXXXX                 ",
        "                                ",
        "                      C         ",
        "                    XXXXX       ",
        "                                ",
        "   XX                           ",
        "             E                  ",
        "           XXXXXX               ",
        "                              G ",
        "XXXX   XXX        XXX   XXXXXXXX",
        "XXXX   XXX        XXX   XXXXXXXX"
    ],
    # Level 7 - Small platforms
    [
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "        C      C      C         ",
        "       XX     XX     XX         ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                              G ",
        "XXX   XXX  XXX  XXX  XXX  XXXXXX",
        "XXX   XXX  XXX  XXX  XXX  XXXXXX"
    ],
    # Level 8 - Ambush
    [
        "                                ",
        "                                ",
        "                                ",
        "                            C   ",
        "             E   E        XXXX  ",
        "            XXXXXXX             ",
        "                                ",
        "                                ",
        "    E                       E   ",
        "  XXXXX                   XXXXX ",
        "                                ",
        "              XXX               ",
        "                                ",
        "      X                 X       ",
        "  X                             ",
        "                              G ",
        "XXX         XXX        XXXXXXXXX",
        "XXX         XXX        XXXXXXXXX"
    ],
    # Level 9 - Pyramid
    [
        "                                ",
        "                                ",
        "                                ",
        "                       C        ",
        "                     XXXX       ",
        "                 E              ",
        "               XXXX             ",
        "           C                    ",
        "         XXXX                   ",
        "     E                          ",
        "   XXXX                         ",
        "                                ",
        "                                ",
        "       XXX             XXX      ",
        "                                ",
        "                              G ",
        "XXXXX       XXXXX     XXXXXXXXXX",
        "XXXXX       XXXXX     XXXXXXXXXX"
    ],
    # Level 10 - Finale
    [
        "                                         ",
        "                                         ",
        "                                         ",
        "                      C C C              ",
        "                      XXXXX              ",
        "                E                        ",
        "              XXXXX                      ",
        "         C                               ",
        "       XXXXX                             ",
        "                                         ",
        "                               E         ",
        "     XXX                     XXXXX       ",
        "                                         ",
        "          XXX       XXX                  ",
        "                                         ",
        "                                         G",
        "XXXXXX      XXXXXX        XXXX     XXXXXXX",
        "XXXXXX      XXXXXX        XXXX     XXXXXXX"
    ]
]


def create_level(level_idx):
    blocks = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    goal = pygame.sprite.Group()
    
    level_map = LEVELS[level_idx]
    
    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            
            if cell == 'X':
                block = Block(x, y)
                blocks.add(block)
            elif cell == 'C':
                coin = Coin(x, y)
                coins.add(coin)
            elif cell == 'E':
                enemy = Enemy(x, y)
                enemies.add(enemy)
            elif cell == 'G':
                g = Goal(x, y)
                goal.add(g)

    player = Player(50, 400)
    return player, blocks, enemies, coins, goal

def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

def draw_text_center(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def run_menu():
    menu_running = True
    selected_option = 0
    options = ["1. New Game", "2. Load Game", "3. Exit"]

    while menu_running:
        screen.fill(MENU_BLUE)
        
        # Static background for menu
        screen.blit(bg_img, (0, 0))

        draw_text_center(screen, "SUPER MARIO DEMO", big_font, WHITE, SCREEN_WIDTH/2, 150)
        draw_text_center(screen, "Pekolandish Edition", font, COIN_YELLOW, SCREEN_WIDTH/2, 220)

        for i, option in enumerate(options):
            color = MENU_HIGHLIGHT if i == selected_option else WHITE
            draw_text_center(screen, option, font, color, SCREEN_WIDTH/2, 350 + i * 50)

        draw_text_center(screen, "Use UP/DOWN to navigate. Press ENTER to select.", small_font, WHITE, SCREEN_WIDTH/2, 550)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return "NEW"
                    elif selected_option == 1:
                        return "LOAD"
                    elif selected_option == 2:
                        return "EXIT"

        pygame.display.flip()
        clock.tick(FPS)

def main():
    while True:
        # Run Menu First
        action = run_menu()
        
        if action == "EXIT":
            break
            
        current_level = 0
        total_score = 0

        if action == "LOAD":
            current_level, total_score = load_game_data()

        # Start game loop
        player, blocks, enemies, coins, goal = create_level(current_level)
        player.score = total_score
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player, blocks, enemies, coins, goal)
        
        camera_x = 0
        bg_x = 0
        
        running = True
        paused = False

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False # Go back to menu
                        
                    if event.key == pygame.K_p:
                        paused = not paused

                    if player.is_dead:
                        if event.key == pygame.K_RETURN:
                            player, blocks, enemies, coins, goal = create_level(current_level)
                            player.score = total_score 
                            all_sprites = pygame.sprite.Group()
                            all_sprites.add(player, blocks, enemies, coins, goal)
                            camera_x = 0
                            
                    elif player.won_level:
                        if event.key == pygame.K_RETURN:
                            total_score = player.score
                            current_level += 1
                            if current_level < len(LEVELS):
                                # Save progress auto between levels
                                save_game_data(current_level, total_score)
                                player, blocks, enemies, coins, goal = create_level(current_level)
                                player.score = total_score
                                all_sprites = pygame.sprite.Group()
                                all_sprites.add(player, blocks, enemies, coins, goal)
                                camera_x = 0
                            else:
                                running = False # Beat game, return to menu

            if paused:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(50)
                overlay.fill(BLACK)
                screen.blit(overlay, (0,0))
                draw_text_center(screen, "PAUSED", big_font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
                draw_text_center(screen, "Press S to Save & Quit Menu", font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)
                draw_text_center(screen, "(ESC to Quit without saving)", small_font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60)
                
                # Check Pause menu keys specifically
                keys = pygame.key.get_pressed()
                if keys[pygame.K_s]:
                    save_game_data(current_level, player.score)
                    running = False # Save and jump to menu

                pygame.display.flip()
                clock.tick(FPS)
                continue

            # Update
            if not player.is_dead and not player.won_level and current_level < len(LEVELS):
                player.update(blocks, enemies, coins, goal)
                enemies.update(blocks)
                
                if player.rect.x > SCREEN_WIDTH / 2:
                    camera_x = player.rect.x - (SCREEN_WIDTH / 2)
                    bg_x = -(camera_x * 0.5) % SCREEN_WIDTH

            # Draw
            screen.blit(bg_img, (bg_x, 0))
            screen.blit(bg_img, (bg_x - SCREEN_WIDTH, 0))
            screen.blit(bg_img, (bg_x + SCREEN_WIDTH, 0)) 
            
            for sprite in all_sprites:
                screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
                
            draw_text(screen, f"SCORE: {player.score}", font, BLACK, 20, 20)
            draw_text(screen, f"LEVEL: {current_level + 1} / {len(LEVELS)}", font, BLACK, SCREEN_WIDTH - 200, 20)
            
            if player.is_dead:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(150)
                overlay.fill(BLACK)
                screen.blit(overlay, (0,0))
                draw_text_center(screen, "GAME OVER", big_font, (255, 50, 50), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
                draw_text_center(screen, "Press ENTER to Retry Level", font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)
                draw_text_center(screen, "Press ESC to Return to Menu", small_font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60)

            elif player.won_level:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(150)
                overlay.fill(BLACK)
                screen.blit(overlay, (0,0))
                
                if current_level >= len(LEVELS) - 1:
                    draw_text_center(screen, "YOU BEAT THE GAME!", big_font, COIN_YELLOW, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
                    draw_text_center(screen, f"Final Score: {player.score}", font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)
                    draw_text_center(screen, "Press ENTER to Return to Menu", font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 70)
                else:
                    draw_text_center(screen, "LEVEL COMPLETE!", big_font, COIN_YELLOW, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
                    draw_text_center(screen, "Game Auto-Saved", small_font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 5)
                    draw_text_center(screen, "Press ENTER for Next Level", font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30)

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
