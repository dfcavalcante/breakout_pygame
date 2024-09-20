import pygame

pygame.init()

# Cores do jogo
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)

# Dimensões da tela do jogo (600x950)
size = (600, 950)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout - 8 Fileiras, 2 Cores por Fileira")

# Texto de pontuação
score_font = pygame.font.Font(None, 44)
score_text_rect = pygame.Rect(0, 0, 600, 50)
score_text_rect.center = (300, 30)

# Jogador (paddle)
player = pygame.Surface((120, 20))
player.fill(COLOR_WHITE)
player_x = 240
player_move_left = False
player_move_right = False

# Bola
ball = pygame.Surface((20, 20))
ball.fill(COLOR_WHITE)
ball_x = 290
ball_y = 440
ball_dx = 2.5
ball_dy = -2.5
ball_speed = 2.2
initial_ball_speed = 2.2
max_ball_speed = 6.0

# Blocos
block_width = 60
block_height = 20
blocks = []

# Cores das linhas de blocos (2 fileiras por cor)
block_colors = [COLOR_RED, COLOR_RED, COLOR_ORANGE, COLOR_ORANGE, COLOR_YELLOW, COLOR_YELLOW, COLOR_GREEN, COLOR_GREEN]

# Ajuste de espaçamento e cálculo de posição centralizada
num_cols = 10
block_spacing_x = 5
block_spacing_y = 5
total_block_width = num_cols * block_width + (num_cols - 1) * block_spacing_x
start_x = (600 - total_block_width) // 2

# Criando a grade de blocos (10 colunas, 8 linhas)
for row in range(8):
    for col in range(10):
        block_x = start_x + col * (block_width + block_spacing_x)
        block_y = row * (block_height + block_spacing_y) + 100
        block_color = block_colors[row]
        blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))

# Pontuação e vidas
score = 0
lives = 1
paddle_hits = 0  # Paddle hits counter

# Função para reiniciar o jogo
def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, score, blocks, lives, ball_speed, paddle_hits
    ball_x = 290
    ball_y = 440
    ball_dx = 2.5
    ball_dy = -2.5
    ball_speed = initial_ball_speed
    paddle_hits = 0
    score = 0
    lives = 1
    blocks.clear()
    for row in range(8):
        for col in range(10):
            block_x = start_x + col * (block_width + block_spacing_x)
            block_y = row * (block_height + block_spacing_y) + 100
            blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))

# Function to increase ball's speed
def increase_ball_speed():
    global ball_speed
    ball_speed = min(ball_speed + 0.5, max_ball_speed)  # Aumenta a velocidade e limita ao máximo

# Game loop
game_loop = True
game_clock = pygame.time.Clock()

while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        # Eventos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_move_left = True
            if event.key == pygame.K_RIGHT:
                player_move_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_move_left = False
            if event.key == pygame.K_RIGHT:
                player_move_right = False

    # Limpar a tela
    screen.fill(COLOR_BLACK)

    # Desenhar blocos
    for block in blocks:
        row_color = block_colors[blocks.index(block) // 10]
        pygame.draw.rect(screen, row_color, block)

    # Movimento da bola
    ball_x += ball_dx * ball_speed
    ball_y += ball_dy * ball_speed

    # Movimento do jogador (paddle)
    if player_move_left and player_x > 0:
        player_x -= 5.5
    if player_move_right and player_x < 480:
        player_x += 5.5

    # Colisão da bola com as paredes
    if ball_x <= 0 or ball_x >= 580:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1

    # Colisão da bola com o paddle
    if ball_y >= 860 and player_x <= ball_x <= player_x + 120:
        ball_dy *= -1
        paddle_hits += 1  # Counts Paddle collisions

        # Incrase ball's speed after 4 hits and them 12 hits
        if paddle_hits == 4 or paddle_hits == 12:
            increase_ball_speed()

    # Colisão da bola com os blocos
    for block in blocks[:]:
        if block.collidepoint(ball_x, ball_y):
            blocks.remove(block)
            ball_dy *= -1
            score += 1

            # Verifica a cor do bloco atingido para aumentar a velocidade
            block_index = blocks.index(block) // 10 if block in blocks else -1
            if block_index in [0, 1]:  # red row
                increase_ball_speed()
            elif block_index in [2, 3]:  # orange row
                increase_ball_speed()

    # Verifica se a bola caiu
    if ball_y > 1000:
        lives += 1
        if lives >= 4:
            reset_game()  # Reiniciar jogo
        else:
            pygame.time.delay(500)  # Atraso de 500 ms para dar tempo de reação
            ball_x = 290
            ball_y = 440
            ball_dx = 2.5
            ball_dy = -2.5

    # Desenhar os objetos na tela
    screen.blit(ball, (ball_x, ball_y))
    screen.blit(player, (player_x, 880))

    # Atualizar o texto da pontuação
    score_text = score_font.render(f'{score}', True, COLOR_WHITE)
    lives_text = score_font.render(f'{lives}', True, COLOR_WHITE)
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, (150, 6))

    # Atualizar a tela
    pygame.display.flip()
    game_clock.tick(60)

pygame.quit()
