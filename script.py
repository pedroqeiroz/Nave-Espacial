import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo Espacial")

# Cores
branco = (255, 255, 255)

# Carregando imagens
fundo = pygame.image.load('background.jpg')
nave_img = pygame.image.load('nave.png')
inimigo_img = pygame.image.load('inimigo.png')
tiro_img = pygame.image.load('tiro.png')
explosao_img = pygame.image.load('explosao.png')

# Carregando sons
som_tiro = pygame.mixer.Sound('tiro.wav')
som_explosao = pygame.mixer.Sound('explosao.wav')

# Variáveis do jogo
nave_x = largura // 2 - 32
nave_y = altura - 64
nave_velocidade = 5

inimigo_x = random.randint(0, largura - 64)
inimigo_y = 0
inimigo_velocidade = 2

tiro_x = 0
tiro_y = 0
tiro_velocidade = 10
tiro_disparado = False

explosao_x = -100
explosao_y = -100
explosao = False

pontuacao = 0
fonte = pygame.font.Font(None, 36)

nivel = 1
max_nivel = 5
velocidade_inicial = 2


# Função para desenhar a nave espacial
def desenhar_nave(x, y):
    tela.blit(nave_img, (x, y))


# Função para desenhar um inimigo
def desenhar_inimigo(x, y):
    tela.blit(inimigo_img, (x, y))


# Função para desenhar um tiro
def desenhar_tiro(x, y):
    tela.blit(tiro_img, (x, y))


# Função para desenhar uma explosão
def desenhar_explosao(x, y):
    tela.blit(explosao_img, (x, y))


# Função para reiniciar o jogo
def reiniciar_jogo():
    global inimigo_x, inimigo_y, tiro_disparado, explosao, pontuacao, nivel, inimigo_velocidade
    inimigo_x = random.randint(0, largura - 64)
    inimigo_y = 0
    tiro_disparado = False
    explosao = False
    pontuacao = 0
    nivel = 1
    inimigo_velocidade = velocidade_inicial


# Loop principal do jogo
jogando = True
inicio = True
reiniciar = False
reiniciar_jogo()
while jogando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if inicio:
                    inicio = False
                if reiniciar:
                    reiniciar = False
                    reiniciar_jogo()
                elif not tiro_disparado and not explosao:
                    tiro_x = nave_x + 16
                    tiro_y = nave_y
                    tiro_disparado = True
                    som_tiro.play()

    if inicio:
        tela.blit(fundo, (0, 0))
        mensagem = fonte.render("Pressione ESPAÇO para iniciar", True, branco)
        tela.blit(mensagem, (largura // 4, altura // 2))
    elif reiniciar:
        tela.blit(fundo, (0, 0))
        mensagem = fonte.render("Fim de jogo. Pontuação: " + str(pontuacao), True, branco)
        tela.blit(mensagem, (largura // 4, altura // 2))
        mensagem = fonte.render("Pressione ESPAÇO para reiniciar", True, branco)
        tela.blit(mensagem, (largura // 4, altura // 2 + 50))
    else:
        tela.blit(fundo, (0, 0)

        # Movimento da nave
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_x > 0:
            nave_x -= nave_velocidade
        if teclas[pygame.K_RIGHT] and nave_x < largura - 64:
            nave_x += nave_velocidade

        # Movimento do inimigo
        inimigo_y += inimigo_velocidade
        if inimigo_y > altura:
            inimigo_x = random.randint(0, largura - 64)
        inimigo_y = 0

        # Movimento do tiro
        if tiro_disparado:
            tiro_y -= tiro_velocidade
        if tiro_y < 0:
            tiro_disparado = False

        # Verificar colisão
        if not explosao:
            colisao_tiro = (
                        tiro_x > inimigo_x and tiro_x < inimigo_x + 64 and tiro_y > inimigo_y and tiro_y < inimigo_y + 64)
        colisao_nave = (
                    nave_x > inimigo_x and nave_x < inimigo_x + 64 and nave_y > inimigo_y and nave_y < inimigo_y + 64)
        if colisao_tiro:
            som_explosao.play()
        explosao_x = inimigo_x
        explosao_y = inimigo_y
        explosao = True
        inimigo_x = random.randint(0, largura - 64)
        inimigo_y = 0
        tiro_disparado = False
        pontuacao += 1
        if colisao_nave:
            som_explosao.play()
        explosao_x = nave_x
        explosao_y = nave_y
        explosao = True
        nave_x = largura // 2 - 32
        nave_y = altura - 64
        inimigo_x = random.randint(0, largura - 64)
        inimigo_y = 0
        tiro_disparado = False
        nivel = 1
        inimigo_velocidade = velocidade_inicial

        # Desenhar elementos na tela
        if explosao:
            desenhar_explosao(explosao_x, explosao_y)
        else:
            desenhar_inimigo(inimigo_x, inimigo_y)
        if tiro_disparado:
            desenhar_tiro(tiro_x, tiro_y)
        desenhar_nave(nave_x, nave_y)

        # Exibir pontuação e nível na tela
        mensagem_pontuacao = fonte.render("Pontuação: " + str(pontuacao), True, branco)
        mensagem_nivel = fonte.render("Nível: " + str(nivel), True, branco)
        tela.blit(mensagem_pontuacao, (10, 10))
        tela.blit(mensagem_nivel, (10, 50))

        # Aumentar a velocidade e o nível a cada 10 pontos
        if pontuacao % 10 == 0 and pontuacao > 0:
            nivel += 1
        inimigo_velocidade += 1

        pygame.display.update()

        # Tela de reinício
        if colisao_nave:
            reiniciar = True
        inicio = False
        tela.fill((0, 0, 0))

        pygame.quit()
