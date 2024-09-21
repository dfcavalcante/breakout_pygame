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
player_width = 60  # Largura inicial do paddle
player_height = 20
player = pygame.Surface((player_width, player_height))
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

# Bordas laterais e superior
left_border = pygame.Rect(20, 0, 20, 850)  # Borda esquerda
right_border = pygame.Rect(660, 0, 20, 850)  # Borda direita
top_border = pygame.Rect(20, 0, 660, 20)  # Borda superior

# Cor das bordas laterais e superior
border_color = COLOR_BLUE  # Ajustado para azul

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
    # Verifica a colisão da bola com a raquete
    if 817 <= ball_y <= 822 and player_x <= ball_x <= player_x + player_width:
        ball_dy *= -1
        paddle_hits += 1

        # Ajuste a direção com base na posição onde a bola colide com a raquete
        hit_pos = ball_x - player_x
        if hit_pos < player_width // 3:  # Esquerda da raquete
            ball_dx = -abs(ball_dx)  # Mover para a esquerda
        elif hit_pos > (2 * player_width) // 3:  # Direita da raquete
            ball_dx = abs(ball_dx)  # Mover para a direita
        else:
            ball_dx = 0  # Se bater no meio, mantém o eixo horizontal

        # Aumenta a velocidade da bola em certos intervalos
        if paddle_hits == 4 or paddle_hits == 12:
            increase_ball_speed()

# Função para aumentar o paddle ao perder vida
def increase_paddle_size():
    global player_width, player
    player_width = 660  # Largura total da tela (menos as bordas)
    player = pygame.Surface((player_width, player_height))
    player.fill(COLOR_BLUE)

# Função para restaurar o tamanho original do paddle
def restore_paddle_size():
    global player_width, player
    player_width = 60  # Largura original do paddle
    player = pygame.Surface((player_width, player_height))
    player.fill(COLOR_BLUE)

# Função para lidar com a perda de vidas
def handle_life_loss():
    global lives, ball_x, ball_y, ball_dx, ball_dy
    lives += 1
    if lives >= 4:
        reset_game()  # Reiniciar jogo se todas as vidas forem perdidas
    else:
        increase_paddle_size()  # Aumentar paddle ao perder vida
        pygame.time.delay(500)  # Atraso de 500 ms para dar tempo de reação
        restore_paddle_size()  # Restaurar o tamanho do paddle após o atraso
        ball_x = 340
        ball_y = 420
        ball_dx = 2.5
        ball_dy = -2.5

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
    pygame.draw.rect(screen, border_color, left_border)
    pygame.draw.rect(screen, border_color, right_border)
    pygame.draw.rect(screen, border_color, top_border)

    # Desenhar blocos
    for i, block in enumerate(blocks):
        pygame.draw.rect(screen, block_colors[i], block)

    # Movimento da bola
    ball_x += ball_dx * ball_speed
    ball_y += ball_dy * ball_speed

    # Movimento do jogador (paddle)
    if player_move_left and player_x > 40:  # Limitando com a borda esquerda
        player_x -= 10
    if player_move_right and player_x < 700 - player_width - 40:  # Limitando com a borda direita
        player_x += 10

    # Colisão da bola com as paredes
    if ball_x <= 40 or ball_x >= 640:
        ball_dx *= -1

    if ball_y <= 40:
        ball_dy *= -1

    # Colisão com o paddle
    ball_paddle_collision()

    # Colisão com os blocos
    for i in range(len(blocks)):
        if blocks[i].collidepoint(ball_x, ball_y):
            ball_dy *= -1
            del blocks[i]  # Remover o bloco usando o índice
            del block_colors[i]  # Remover a cor do índice correspondente
            if ball_x < 350:
                score_left += 1
            else:
                score_right += 1
            break

    # Verificar se a bola caiu abaixo do paddle
    if ball_y > 850:
        handle_life_loss()

    # Desenhar paddle e bola
    screen.blit(player, (player_x, 820))
    screen.blit(ball, (ball_x, ball_y))

    # Atualizar e desenhar placar
    score_text_left = score_font.render(str(score_left), True, COLOR_WHITE)
    score_text_right = score_font.render(str(score_right), True, COLOR_WHITE)
    screen.blit(score_text_left, score_text_rect_left)
    screen.blit(score_text_right, score_text_rect_right)

    # Atualizar a tela
    pygame.display.flip()

    # FPS
    game_clock.tick(60)

# Encerrar o jogo
pygame.quit()
