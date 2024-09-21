import pygame

pygame.init()

# Cores do jogo
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 120, 255)
COLOR_GRAY = (200, 200, 200)  # Cor das bordas e da moldura
COLOR_RED = (255, 0, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)

# Dimensões da tela do jogo (700x850)
size = (700, 850)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Retro Style")

# Texto de pontuação
score_font = pygame.font.Font(None, 80)  # Fonte maior e retrô
score_text_rect_left = pygame.Rect(70, 20, 100, 100)  # Ajuste da posição do placar esquerdo
score_text_rect_right = pygame.Rect(500, 20, 100, 100)  # Ajuste da posição do placar direito

# Jogador (paddle) - agora menor e azul
player = pygame.Surface((60, 20))
player.fill(COLOR_BLUE)
player_x = 320
player_move_left = False
player_move_right = False

# Bola
ball = pygame.Surface((10, 10))  # Bola um pouco menor
ball.fill(COLOR_WHITE)
ball_x = 340
ball_y = 420
ball_dx = 2.5
ball_dy = -2.5
ball_speed = 2.2
initial_ball_speed = 2.2
max_ball_speed = 6.0

# Blocos (estilo retrô)
block_width = 42
block_height = 12
blocks = []
block_colors = []

# Cores das linhas de blocos (2 fileiras por cor)
row_colors = [COLOR_RED, COLOR_RED, COLOR_ORANGE, COLOR_ORANGE, COLOR_GREEN, COLOR_GREEN, COLOR_YELLOW, COLOR_YELLOW]

# Ajuste de espaçamento e cálculo de posição centralizada
num_cols = 14  # Agora com mais colunas para ser fiel ao design
block_spacing_x = 3
block_spacing_y = 3
total_block_width = num_cols * block_width + (num_cols - 1) * block_spacing_x
start_x = (700 - total_block_width) // 2

# Criando a grade de blocos (14 colunas, 8 linhas) e atribuindo cores fixas
for row in range(8):
    for col in range(14):
        block_x = start_x + col * (block_width + block_spacing_x)
        block_y = row * (block_height + block_spacing_y) + 150  # Ajustando a altura
        blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))
        block_colors.append(row_colors[row])  # Mantém a cor da fileira para o bloco correspondente

# Bordas (laterais e superior)
left_border = pygame.Rect(20, 0, 20, 850)  # Borda esquerda
right_border = pygame.Rect(660, 0, 20, 850)  # Borda direita
top_border = pygame.Rect(20, 0, 660, 20)  # Borda superior

# Pontuação e vidas
score_left = 0
score_right = 0
lives = 1
paddle_hits = 0  # Contador de colisões com a raquete

# Função para reiniciar o jogo
def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, score_left, score_right, blocks, block_colors, lives, ball_speed, paddle_hits
    ball_x = 340
    ball_y = 420
    ball_dx = 2.5
    ball_dy = -2.5
    ball_speed = initial_ball_speed
    paddle_hits = 0
    score_left = 0
    score_right = 0
    lives = 1
    blocks.clear()
    block_colors.clear()
    for row in range(8):
        for col in range(14):
            block_x = start_x + col * (block_width + block_spacing_x)
            block_y = row * (block_height + block_spacing_y) + 150
            blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))
            block_colors.append(row_colors[row])

# Função para aumentar a velocidade da bola
def increase_ball_speed():
    global ball_speed
    ball_speed = min(ball_speed + 0.5, max_ball_speed)  # Aumenta a velocidade e limita ao máximo

# Função para verificar colisão com a raquete e ajustar o ângulo da bola
def ball_paddle_collision():
    global ball_dy, ball_dx, paddle_hits
    if 817 <= ball_y <= 822  and player_x <= ball_x <= player_x + 62:
        ball_dy *= -1
        paddle_hits += 1
        hit_paddle.play()

        # Ajuste a direção com base na posição onde a bola colide com a raquete
        hit_pos = ball_x - player_x
        if hit_pos < 20:  # Esquerda da raquete
            ball_dx = -abs(ball_dx)  # Mover para a esquerda
        elif hit_pos > 40:  # Direita da raquete
            ball_dx = abs(ball_dx)  # Mover para a direita

        if paddle_hits == 4 or paddle_hits == 12:
            increase_ball_speed()

def decrease_paddle_size():
    if ball_y <= 20:
        player = pygame.Surface((30, 20))

# Sound Effects
hit_wall = pygame.mixer.Sound('Sounds/ball_hit_wall.wav')
hit_block = pygame.mixer.Sound('Sounds/ball_hit_block.wav')
hit_paddle = pygame.mixer.Sound('Sounds/ball_hit_paddle.wav')

# Loop do jogo
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

    # Desenhar bordas
    pygame.draw.rect(screen, COLOR_GRAY, left_border)
    pygame.draw.rect(screen, COLOR_GRAY, right_border)
    pygame.draw.rect(screen, COLOR_GRAY, top_border)

    # Desenhar blocos
    for i, block in enumerate(blocks):
        pygame.draw.rect(screen, block_colors[i], block)

    # Movimento da bola
    ball_x += ball_dx * ball_speed
    ball_y += ball_dy * ball_speed

    # Movimento do jogador (paddle)
    if player_move_left and player_x > 40:  # Limitando com a borda esquerda
        player_x -= 10
    if player_move_right and player_x < 600:  # Limitando com a borda direita
        player_x += 10

    # Colisão da bola com as paredes
    if ball_x <= 40 or ball_x >= 640:
        ball_dx *= -1
        hit_wall.play()
    if ball_y <= 20:
        ball_dy *= -1
        hit_wall.play()

    # Colisão da bola com o paddle
    ball_paddle_collision()


    # Colisão da bola com os blocos
    for block in blocks[:]:
        if block.collidepoint(ball_x, ball_y):
            hit_block.play()
            index = blocks.index(block)
            blocks.remove(block)
            block_colors.pop(index)  # Remove a cor associada ao bloco
            ball_dy *= -1
            score_left += 1  # Incrementa o placar da esquerda

    # Verifica se a bola caiu
    if ball_y > 1000:
        lives += 1
        if lives >= 4:
            reset_game()  # Reiniciar jogo
        else:
            pygame.time.delay(500)  # Atraso de 500 ms para dar tempo de reação
            ball_x = 340
            ball_y = 420
            ball_dx = 2.5
            ball_dy = -2.5

    # Desenhar os objetos na tela
    screen.blit(ball, (ball_x, ball_y))
    screen.blit(player, (player_x, 830))

    # Desenhar o placar
    score_text_left = score_font.render(f"{score_left:03}", True, COLOR_WHITE)
    score_text_right = score_font.render(f"{lives}", True, COLOR_WHITE)
    screen.blit(score_text_left, score_text_rect_left)
    screen.blit(score_text_right, score_text_rect_right)

    pygame.display.flip()

    game_clock.tick(60)  # 60 FPS

pygame.quit()