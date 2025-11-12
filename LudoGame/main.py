import pygame
import random
import sys
import os
import math

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title
pygame.display.set_caption("Ludo Game")

# Asset loading
script_dir = os.path.dirname(__file__)
assets_dir = os.path.join(script_dir, 'assets')
dice_images = [pygame.image.load(os.path.join(assets_dir, f"dice-{i}.png")) for i in range(1, 7)]
dice_value = 1

# Player turn
player_colors = [RED, GREEN, YELLOW, BLUE]
current_player_index = 0

# Game state
game_state = "roll" # roll, select

# Paths for each color
paths = {
    RED: [(260, 40), (260, 80), (260, 120), (260, 160), (260, 200), (200, 260), (160, 260), (120, 260), (80, 260), (40, 260), (40, 300), (40, 340), (80, 340), (120, 340), (160, 340), (200, 340), (260, 400), (260, 440), (260, 480), (260, 520), (260, 560), (300, 560), (340, 560), (340, 520), (340, 480), (340, 440), (340, 400), (400, 340), (440, 340), (480, 340), (520, 340), (560, 340), (560, 300), (560, 260), (520, 260), (480, 260), (440, 260), (400, 260), (340, 200), (340, 160), (340, 120), (340, 80), (340, 40), (300, 40)],
    GREEN: [(560, 260), (520, 260), (480, 260), (440, 260), (400, 260), (340, 200), (340, 160), (340, 120), (340, 80), (340, 40), (300, 40), (260, 40), (260, 80), (260, 120), (260, 160), (260, 200), (200, 260), (160, 260), (120, 260), (80, 260), (40, 260), (40, 300), (40, 340), (80, 340), (120, 340), (160, 340), (200, 340), (260, 400), (260, 440), (260, 480), (260, 520), (260, 560), (300, 560), (340, 560), (340, 520), (340, 480), (340, 440), (340, 400), (400, 340), (440, 340), (480, 340), (520, 340), (560, 340), (560, 300)],
    YELLOW: [(340, 560), (340, 520), (340, 480), (340, 440), (340, 400), (400, 340), (440, 340), (480, 340), (520, 340), (560, 340), (560, 300), (560, 260), (520, 260), (480, 260), (440, 260), (400, 260), (340, 200), (340, 160), (340, 120), (340, 80), (340, 40), (300, 40), (260, 40), (260, 80), (260, 120), (260, 160), (260, 200), (200, 260), (160, 260), (120, 260), (80, 260), (40, 260), (40, 300), (40, 340), (80, 340), (120, 340), (160, 340), (200, 340), (260, 400), (260, 440), (260, 480), (260, 520), (260, 560), (300, 560)],
    BLUE: [(40, 340), (80, 340), (120, 340), (160, 340), (200, 340), (260, 400), (260, 440), (260, 480), (260, 520), (260, 560), (300, 560), (340, 560), (340, 520), (340, 480), (340, 440), (340, 400), (400, 340), (440, 340), (480, 340), (520, 340), (560, 340), (560, 300), (560, 260), (520, 260), (480, 260), (440, 260), (400, 260), (340, 200), (340, 160), (340, 120), (340, 80), (340, 40), (300, 40), (260, 40), (260, 80), (260, 120), (260, 160), (260, 200), (200, 260), (160, 260), (120, 260), (80, 260), (40, 260), (40, 300)]
}
home_paths = {
    RED: [(300, 80), (300, 120), (300, 160), (300, 200), (300, 240)],
    GREEN: [(520, 300), (480, 300), (440, 300), (400, 300), (360, 300)],
    YELLOW: [(300, 520), (300, 480), (300, 440), (300, 400), (300, 360)],
    BLUE: [(80, 300), (120, 300), (160, 300), (200, 300), (240, 300)]
}
safe_squares = [(260, 40), (40, 300), (340, 560), (560, 260)]

class Token:
    def __init__(self, color, home_x, home_y):
        self.color = color
        self.x, self.y = home_x, home_y
        self.home_x, self.home_y = home_x, home_y
        self.radius = 20
        self.state = 'home'
        self.path_index = -1

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, steps):
        if self.state == 'active':
            self.path_index += steps
            if self.path_index >= len(paths[self.color]):
                self.state = 'home_path'
                self.path_index -= len(paths[self.color])
                if self.path_index >= len(home_paths[self.color]):
                    self.state = 'finished'
                    self.x, self.y = -100, -100
                else:
                    self.x, self.y = home_paths[self.color][self.path_index]
            else:
                self.x, self.y = paths[self.color][self.path_index]
            self.check_capture()
        elif self.state == 'home_path':
            self.path_index += steps
            if self.path_index >= len(home_paths[self.color]):
                self.state = 'finished'
                self.x, self.y = -100, -100
            else:
                self.x, self.y = home_paths[self.color][self.path_index]

    def check_capture(self):
        if (self.x, self.y) in safe_squares:
            return
        for other_token in tokens:
            if other_token.color != self.color and (other_token.x, other_token.y) == (self.x, self.y):
                other_token.state = 'home'
                other_token.x, other_token.y = other_token.home_x, other_token.home_y
                other_token.path_index = -1

tokens = [Token(color, pos[0], pos[1]) for color, positions in {
    RED: [(60, 60), (180, 60), (60, 180), (180, 180)],
    GREEN: [(420, 60), (540, 60), (420, 180), (540, 180)],
    BLUE: [(60, 420), (180, 420), (60, 540), (180, 540)],
    YELLOW: [(420, 420), (540, 420), (420, 540), (540, 540)],
}.items() for pos in positions]

def draw_board():
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (0, 0, 240, 240))
    pygame.draw.rect(screen, GREEN, (360, 0, 240, 240))
    pygame.draw.rect(screen, BLUE, (0, 360, 240, 240))
    pygame.draw.rect(screen, YELLOW, (360, 360, 240, 240))
    pygame.draw.rect(screen, BLACK, (240, 0, 120, 600))
    pygame.draw.rect(screen, BLACK, (0, 240, 600, 120))
    pygame.draw.polygon(screen, RED, [(240, 300), (300, 240), (300, 300)])
    pygame.draw.polygon(screen, GREEN, [(300, 240), (360, 300), (300, 300)])
    pygame.draw.polygon(screen, BLUE, [(300, 360), (240, 300), (300, 300)])
    pygame.draw.polygon(screen, YELLOW, [(360, 300), (300, 360), (300, 300)])
    for x, y in safe_squares:
        pygame.draw.circle(screen, GREY, (x, y), 10)

def draw_tokens():
    for token in tokens:
        token.draw()

def check_win():
    for color in player_colors:
        if all(token.state == 'finished' for token in tokens if token.color == color):
            return color
    return None

def roll_dice():
    global dice_value, game_state
    dice_value = random.randint(1, 6)
    game_state = "select"

def get_clicked_token(pos):
    for token in tokens:
        dist = math.sqrt((token.x - pos[0])**2 + (token.y - pos[1])**2)
        if dist <= token.radius:
            return token
    return None

def draw_game_state_text():
    font = pygame.font.Font(None, 36)
    color_name = {RED: "Red", GREEN: "Green", BLUE: "Blue", YELLOW: "Yellow"}
    player_name = color_name[player_colors[current_player_index]]
    if game_state == "roll":
        text = font.render(f"{player_name}'s turn. Click to roll.", True, BLACK)
    else:
        text = font.render(f"{player_name} rolled a {dice_value}. Select a token.", True, BLACK)
    screen.blit(text, (10, 10))


# Game loop
running = True
winner = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not winner:
            if game_state == "roll":
                roll_dice()
            elif game_state == "select":
                pos = pygame.mouse.get_pos()
                token = get_clicked_token(pos)
                if token and token.color == player_colors[current_player_index]:
                    if (token.state == 'home' and dice_value == 6) or token.state == 'active' or token.state == 'home_path':
                        if token.state == 'home':
                            token.state = 'active'
                            token.path_index = 0
                            token.x, token.y = paths[token.color][0]
                        else:
                            token.move(dice_value)

                        if dice_value != 6:
                            current_player_index = (current_player_index + 1) % len(player_colors)
                        game_state = "roll"
                        winner = check_win()


    draw_board()
    draw_tokens()
    screen.blit(dice_images[dice_value - 1], (270, 270))
    draw_game_state_text()

    if winner:
        font = pygame.font.Font(None, 74)
        winner_color_name = {RED: "Red", GREEN: "Green", BLUE: "Blue", YELLOW: "Yellow"}
        text = font.render(f"{winner_color_name[winner]} Wins!", True, BLACK)
        screen.blit(text, (150, 250))


    pygame.display.update()

pygame.quit()
sys.exit()
