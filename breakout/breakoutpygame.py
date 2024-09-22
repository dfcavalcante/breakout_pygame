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
size = (600, 850)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Retro Style")

# Texto de pontuação
score_font = pygame.font.Font(None, 80)  # Fonte maior e retrô
score_text_rect_left = pygame.Rect(70, 20, 100, 100)  # Ajuste da posição do placar esquerdo
score_text_rect_right = pygame.Rect(500, 20, 100, 100)  # Ajuste da posição do placar direito

# Tamanho inicial da raquete
initial_paddle_width = 60
initial_paddle_height = 20
paddle_width = initial_paddle_width
paddle_height = initial_paddle_height

# Jogador (paddle)
player_surface = pygame.Surface((paddle_width, paddle_height))
player_surface.fill(COLOR_BLUE)
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
start_x = (600 - total_block_width) // 2

# Criando a grade de blocos (14 colunas, 8 linhas) e atribuindo cores fixas
for row in range(8):
    for col in range(14):
        block_x = start_x + col * (block_width + block_spacing_x)
        block_y = row * (block_height + block_spacing_y) + 150  # Ajustando a altura
        blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))
        block_colors.append(row_colors[row])  # Mantém a cor da fileira para o bloco correspondente

# Bordas (laterais e superior)
left_border = pygame.Rect(20, 0, 20, 850)  # Borda esquerda
right_border = pygame.Rect(560, 0, 20, 850)  # Borda direita
top_border = pygame.Rect(20, 0, 560, 20)  # Borda superior

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

# Função para corrigir colisão com a raquete e impedir colisão múltipla
def ball_paddle_collision():
    global ball_dy, ball_dx, paddle_hits
    # Verifica se a bola colide com a raquete
    if player_x <= ball_x <= player_x + paddle_width and ball_y + 10 >= 830:  # Corrigido para verificar a posição y corretamente
        ball_dy *= -1  # Inverte a direção vertical da bola
        paddle_hits += 1
        hit_paddle.play()

        # Ajuste da direção horizontal da bola com base na posição onde a bola colide com a raquete
        hit_pos = ball_x - player_x
        if hit_pos < paddle_width // 3:  # Se a bola atinge a esquerda da raquete
            ball_dx = -abs(ball_dx)  # Direciona a bola para a esquerda
        elif hit_pos > 2 * paddle_width // 3:  # Se a bola atinge a direita da raquete
            ball_dx = abs(ball_dx)  # Direciona a bola para a direita

        # Aumenta a velocidade da bola a cada 4 e 12 colisões com a raquete
        if paddle_hits == 4 or paddle_hits == 12:
            increase_ball_speed()


first_top_collision = True  # Variável para verificar a primeira colisão com a parede de cima

# Sound Effects
hit_wall = pygame.mixer.Sound('assets/ball_hit_wall.wav')
hit_block = pygame.mixer.Sound('assets/ball_hit_block.wav')
hit_paddle = pygame.mixer.Sound('assets/ball_hit_paddle.wav')

# Loop do jogo
game_loop = True
game_clock = pygame.time.Clock()

# Função modificada para aumentar a pontuação com base na cor do bloco
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

# Variável para verificar se a bola está se movendo para baixo
ball_moving_down = False

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
    if player_move_right and player_x < 500:  # Limitando com a borda direita
        player_x += 10

    # Colisão da bola com as paredes
    # Corrige colisão da bola com as paredes laterais

    if ball_x <= 40:  # Colisão com a parede esquerda
        ball_dx = abs(ball_dx)  # Garante que a bola sempre vai para a direita após colidir com a parede esquerda
        hit_wall.play()

    elif ball_x >= 560:  # Colisão com a parede direita
        ball_dx = -abs(ball_dx)  # Garante que a bola sempre vai para a esquerda após colidir com a parede direita
        hit_wall.play()

    # Corrige colisão da bola com a parte superior
    if ball_y <= 20:  # Colisão com o topo
        ball_dy = abs(
            ball_dy)  # Garante que a bola sempre vai para baixo após colidir com o topo
        hit_wall.play()

        if first_top_collision:
            # Se for a primeira colisão, diminui o tamanho da raquete
            paddle_width = 40  # Redefine o tamanho da raquete
            player_surface = pygame.Surface(
                (paddle_width, paddle_height))  # Redesenha a raquete
            player_surface.fill(COLOR_BLUE)  # Preenche a raquete com a cor
            first_top_collision = False  # Marca que a colisão já ocorreu

    # Impede que a bola atinja blocos ao descer
    if not ball_moving_down:  # Verifica se a bola está subindo
        for block in blocks[:]:
            if block.collidepoint(ball_x, ball_y):
                index = blocks.index(block)
                block_color = block_colors[index]
                blocks.remove(block)
                block_colors.pop(index)  # Remove a cor associada ao bloco

                # Atualiza a pontuação com base na cor do bloco destruído
                update_score_by_block_color(block_color)

                # Se a bola está subindo, rebate, senão atravessa os blocos
                if not ball_moving_down:
                    ball_dy *= -1  # Rebate a bola apenas se estiver subindo
                    hit_block.play()

    # Colisão da bola com o paddle
    ball_paddle_collision()

    # Verifica se a bola está subindo ou descendo
    if ball_dy > 0:
        ball_moving_down = True
    else:
        ball_moving_down = False

    # Colisão da bola com os blocos (ajustado para a bola atravessar blocos quando está descendo)
    for block in blocks[:]:
        if block.collidepoint(ball_x, ball_y):
            index = blocks.index(block)
            block_color = block_colors[index]
            blocks.remove(block)
            block_colors.pop(index)  # Remove a cor associada ao bloco

            # Atualiza a pontuação com base na cor do bloco destruído
            update_score_by_block_color(block_color)

            # Se a bola está subindo, rebate, senão atravessa os blocos
            if not ball_moving_down:
                ball_dy *= -1
                hit_block.play()

    # Verifica se a bola caiu
    if ball_y > 1000:
        lives += 1
        first_top_collision = True
        paddle_width = initial_paddle_width  # Redefinir o tamanho da raquete
        paddle_height = initial_paddle_height  # Redefinir o tamanho da raquete
        player_surface = pygame.Surface((paddle_width, paddle_height))  # Redesenhar a raquete
        player_surface.fill(COLOR_BLUE)  # Preencher a nova raquete com a cor
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
    screen.blit(player_surface, (player_x, 830))

    # Desenhar o placar
    score_text_left = score_font.render(f"{score_left:03}", True, COLOR_WHITE)
    score_text_right = score_font.render(f"{lives}", True, COLOR_WHITE)
    screen.blit(score_text_left, score_text_rect_left)
    screen.blit(score_text_right, score_text_rect_right)

    pygame.display.flip()

    game_clock.tick(60)  # 60 FPS

pygame.quit()