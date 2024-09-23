import pygame

pygame.init()

# game colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 120, 255)
COLOR_GRAY = (200, 200, 200)  # border and frame color
COLOR_RED = (255, 0, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)

# screen dimensions (700x850)
size = (600, 850)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Retro Style")

# score text
score_font = pygame.font.Font(None, 80)  # retro-style font
lives_font = pygame.font.Font(None, 40)  # font for lives
score_text_rect_left = pygame.Rect(70, 20, 100, 100)  # left score position
score_text_rect_right = pygame.Rect(500, 20, 100, 100)  # right score position

# initial paddle size
initial_paddle_width = 60
initial_paddle_height = 20
paddle_width = initial_paddle_width
paddle_height = initial_paddle_height

# player (paddle)
player_surface = pygame.Surface((paddle_width, paddle_height))
player_surface.fill(COLOR_BLUE)
player_x = 320
player_move_left = False
player_move_right = False

# ball
ball = pygame.Surface((10, 10))  # smaller ball size
ball.fill(COLOR_WHITE)
ball_x = 340
ball_y = 420
ball_dx = 2.5
ball_dy = -2.5
ball_speed = 2.2
initial_ball_speed = 2.2
max_ball_speed = 6.0

# blocks (retro style)
block_width = 42
block_height = 12
blocks = []
block_colors = []

# row colors (2 rows per color)
row_colors = [COLOR_RED, COLOR_RED, COLOR_ORANGE, COLOR_ORANGE, COLOR_GREEN,
              COLOR_GREEN, COLOR_YELLOW, COLOR_YELLOW]

# spacing and central positioning
num_cols = 14  # more columns for the design
block_spacing_x = 3
block_spacing_y = 3
total_block_width = num_cols * block_width + (num_cols - 1) * block_spacing_x
start_x = (600 - total_block_width) // 2

# create block grid (14 columns, 8 rows) and assign fixed colors
def create_blocks():
    blocks.clear()
    block_colors.clear()
    for row in range(8):
        for col in range(14):
            block_x = start_x + col * (block_width + block_spacing_x)
            block_y = row * (block_height + block_spacing_y) + 150  # adjusted height
            blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))
            block_colors.append(row_colors[row])  # assign color for each block

create_blocks()

# borders (sides and top)
left_border = pygame.Rect(20, 0, 20, 850)  # left border
right_border = pygame.Rect(560, 0, 20, 850)  # right border
top_border = pygame.Rect(20, 0, 560, 20)  # top border

# score and lives
score_left = 0
lives = 3
paddle_hits = 0  # paddle collision counter

# Safe mode
in_safe_mode = False

# reset game function
def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, score_left, lives, ball_speed, paddle_hits, in_safe_mode, paddle_width, player_surface, player_x
    ball_x = 340
    ball_y = 420
    ball_dx = 2.5
    ball_dy = -2.5
    ball_speed = initial_ball_speed
    paddle_hits = 0
    score_left = 0
    lives = 3
    in_safe_mode = False
    paddle_width = initial_paddle_width
    player_surface = pygame.Surface((paddle_width, paddle_height))
    player_surface.fill(COLOR_BLUE)
    player_x = (600 - paddle_width) // 2  # centralize paddle
    create_blocks()

# increase ball speed function
def increase_ball_speed():
    global ball_speed
    ball_speed = min(ball_speed + 0.5, max_ball_speed)

# handle paddle collision
def ball_paddle_collision():
    global ball_dy, ball_dx, paddle_hits
    if player_x <= ball_x <= player_x + paddle_width and ball_y + 10 >= 830:
        ball_dy *= -1
        paddle_hits += 1

        hit_pos = ball_x - player_x
        if hit_pos < paddle_width // 3:
            ball_dx = -abs(ball_dx)
        elif hit_pos > 2 * paddle_width // 3:
            ball_dx = abs(ball_dx)

        if paddle_hits == 4 or paddle_hits == 12:
            increase_ball_speed()

# sound effects (you need to ensure the files exist in your project)
hit_wall = pygame.mixer.Sound('breakout/assets/ball_hit_wall.wav')
hit_block = pygame.mixer.Sound('breakout/assets/ball_hit_block.wav')
hit_paddle = pygame.mixer.Sound('breakout/assets/ball_hit_paddle.wav')

# game loop
game_loop = True
game_clock = pygame.time.Clock()

# update score based on block color
def update_score_by_block_color(color):
    global score_left
    if color == COLOR_YELLOW:
        score_left += 1
    elif color == COLOR_GREEN:
        score_left += 3
    elif color == COLOR_ORANGE:
        score_left += 5
    elif color == COLOR_RED:
        score_left += 7

ball_moving_down = False  # check if ball is moving down

while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not in_safe_mode:
                player_move_left = True
            if event.key == pygame.K_RIGHT and not in_safe_mode:
                player_move_right = True
            if event.key == pygame.K_SPACE and in_safe_mode:
                reset_game()  # Exit safe mode and reset game

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_move_left = False
            if event.key == pygame.K_RIGHT:
                player_move_right = False

    # clear screen
    screen.fill(COLOR_BLACK)

    # draw borders
    pygame.draw.rect(screen, COLOR_GRAY, left_border)
    pygame.draw.rect(screen, COLOR_GRAY, right_border)
    pygame.draw.rect(screen, COLOR_GRAY, top_border)

    # draw blocks
    for i, block in enumerate(blocks):
        pygame.draw.rect(screen, block_colors[i], block)

    # ball movement
    ball_x += ball_dx * ball_speed
    ball_y += ball_dy * ball_speed

    # player movement (only if not in safe mode)
    if not in_safe_mode:
        if player_move_left and player_x > 40:
            player_x -= 10
        if player_move_right and player_x < 500:
            player_x += 10

    # ball-wall collision
    if ball_x <= 40:
        ball_dx = abs(ball_dx)
        hit_wall.play()

    elif ball_x >= 560:
        ball_dx = -abs(ball_dx)
        hit_wall.play()

    if ball_y <= 20:
        ball_dy = abs(ball_dy)
        hit_wall.play()

    # Safe mode mechanics
    if in_safe_mode:
        paddle_width = 550  # Extend paddle across the entire screen
        player_x = 30  # Center the paddle across the entire width
        player_surface = pygame.Surface((paddle_width, paddle_height))
        player_surface.fill(COLOR_BLUE)

    # ball-paddle collision
    ball_paddle_collision()

    # check if ball is moving down
    ball_moving_down = ball_dy > 0

    # ball-block collision
    if not in_safe_mode:  # Only destroy blocks if not in safe mode
        for block in blocks[:]:
            if block.collidepoint(ball_x, ball_y):
                index = blocks.index(block)
                block_color = block_colors[index]
                blocks.remove(block)
                block_colors.pop(index)
                update_score_by_block_color(block_color)
                ball_dy *= -1
                hit_block.play()

    # ball falls off bottom of screen
    if ball_y > 850:
        lives -= 1
        if lives <= 0 and not in_safe_mode:
            in_safe_mode = True  # Activate safe mode
            paddle_width = 540
            player_surface = pygame.Surface((paddle_width, paddle_height))
            player_surface.fill(COLOR_BLUE)
            player_x = 30  # Center the paddle
            create_blocks()  # Restore all blocks
            ball_speed = initial_ball_speed  # Reset ball speed
            ball_x = 340  # Reset ball position
            ball_y = 420
        elif not in_safe_mode:
            ball_x = 340
            ball_y = 420
            ball_dx = 2.5
            ball_dy = -2.5
            ball_speed = initial_ball_speed
            paddle_hits = 0

    # draw ball and paddle
    screen.blit(ball, (ball_x, ball_y))
    screen.blit(player_surface, (player_x, 830))

    # render scores and lives
    score_text_left = score_font.render(str(score_left), True, COLOR_WHITE)
    screen.blit(score_text_left, score_text_rect_left)

    lives_text = lives_font.render(f"{lives}", True, COLOR_WHITE)
    screen.blit(lives_text, (470, 30))

    pygame.display.update()
    game_clock.tick(60)

pygame.quit()
