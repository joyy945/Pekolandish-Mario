import codecs
import os

with codecs.open("main.py", 'r', 'utf-8') as f:
    content = f.read()

# Replace load_image block
old_load = """def load_image(name, size=None, colorkey=None):
    path = os.path.join('assets', name)
    try:
        image = pygame.image.load(path).convert()
        if size:
            image = pygame.transform.scale(image, size)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0)) # Grab top-left pixel color for perfect background removal
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    except pygame.error as message:
        print(f"Cannot load image: {name}")
        surf = pygame.Surface(size if size else (32, 32))
        surf.fill(PLAYER_RED)
        return surf

# Load all game assets
player_img = load_image('player.png', (32, 40), (255, 0, 255))
enemy_img = load_image('enemy.png', (32, 32), (255, 0, 255))
block_img = load_image('block.png', (TILE_SIZE, TILE_SIZE))
coin_img = load_image('coin.png', (24, 24), (255, 0, 255))"""

new_load = """def load_image(name, size=None):
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
coin_img = load_image('coin.png', (24, 24))"""

if old_load in content:
    content = content.replace(old_load, new_load)
else:
    print("Warning: Could not find old load_image block to replace.")

# Replace LEVELS block
start_idx = content.find("LEVELS = [")
end_idx = content.find("def create_level(level_idx):", start_idx)

if start_idx != -1 and end_idx != -1:
    new_levels = """LEVELS = [
    # Level 1
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
    # Level 2
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
        "                                ",
        "  XXXX   XXXX  XXXX   XXXX    G ",
        "XXXXXX   XXXX  XXXX   XXXXXXXXXX",
        "XXXXXX   XXXX  XXXX   XXXXXXXXXX"
    ],
    # Level 3
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
        "                                ",
        "               E                ",
        "                              G ",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ],
    # Level 4
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
    # Level 5
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
        "     XX              XX         ",
        "                              G ",
        "XXXXX                  XXXXXXXXX",
        "XXXXX                  XXXXXXXXX"
    ],
    # Level 6
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
    # Level 7
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
        "XXX   XX   XX   XX   XX   XXXXXX",
        "XXX   XX   XX   XX   XX   XXXXXX"
    ],
    # Level 8
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
        "      X                         ",
        "  X                             ",
        "                              G ",
        "XXX                        XXXXX",
        "XXX                        XXXXX"
    ],
    # Level 9
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
        "       XX                       ",
        "                                ",
        "                              G ",
        "XXXXX                         XX",
        "XXXXX                         XX"
    ],
    # Level 10
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
        "     XX                      XXXXX       ",
        "                                         ",
        "          XX        XX                   ",
        "                                         ",
        "                                         G",
        "XXXXXX      XXXXXX        XXXX     XXXXXXX",
        "XXXXXX      XXXXXX        XXXX     XXXXXXX"
    ]
]

"""
    content = content[:start_idx] + new_levels + content[end_idx:]
else:
    print("Warning: Could not find LEVELS to replace.")

with codecs.open("main.py", 'w', 'utf-8') as f:
    f.write(content)
print("main.py patched successfully")
