# Versão 1.0
# Importando libraries

import pygame
import os
import subprocess
import random
import sys

pygame.init()  # Iniciando Pygame
pygame.font.init()  # Iniciando fontes

# Tamanho da janela
largura, altura = 360, 640

# Mostra a tela, atrelada largura x altura
display = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Inimigos da Raiva")

# Carregando Sprites
carro_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "carro.png")), (150, 150))  # Player Sprite
dog1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cao1.png")), (60, 60))  # Inimigo 01
dog2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cao2.png")), (60, 60))  # Inimigo 02
dog3 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cao3.png")), (60, 60))  # Inimigo 03
vac = pygame.image.load(os.path.join("assets", "vacina0.png"))  # Projétil 
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")), (largura, altura))  # Fundo COPYRIGHT: wwwdavidstenfors.com

# Carregando Efeitos Sonoros
disparar = pygame.mixer.Sound(os.path.join("SFX", "Shoot_00.mp3"))
dano_player = pygame.mixer.Sound(os.path.join("SFX", "Hit_02.mp3"))
morte_player = pygame.mixer.Sound(os.path.join("SFX", "Hero_Death_00.mp3"))
dano_chefe = pygame.mixer.Sound(os.path.join("SFX", "Hit_03.mp3"))
morte_chefe = pygame.mixer.Sound(os.path.join("SFX", "Explosion_03.mp3"))
morte_inimigo = pygame.mixer.Sound(os.path.join("SFX", "Hit_00.mp3"))

# Projétil 
class Proj(pygame.sprite.Sprite):
    def __init__(self, x, y, img=vac):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = -7  # Vel. negativa para o projétil ir em direção a y

    def move(self):
        self.rect.y += self.vel
        if self.rect.y < 0:  # Projétil despawna ao sair da tela
            self.kill()

    def update(self):
        self.move()

# Player
class Player(pygame.sprite.Sprite): 
    def __init__(self, x, y, vida=3):
        super().__init__()
        self.x = x # Coord. inicial na pos. x
        self.y = y # Coord. inicial na pos. y
        self.vidas = vida 
        self.player_img = carro_img
        self.rect = self.player_img.get_rect(topleft=(x, y)) # 'Rect' -> responsável por Coord. retangulares
        self.mask = pygame.mask.from_surface(self.player_img) # Cria uma máscara para lidar com colisões de forma precisa
        self.proj = pygame.sprite.Group()  # Guardar os projéteis  

    def draw(self, display): # Desenha o player e projéteis
        display.blit(self.player_img, self.rect.topleft)
        self.proj.draw(display) 
    
    def disparar(self): # Lida com disparo de projéteis do player
        projetil = Proj(self.rect.centerx, self.rect.top, vac)                
        self.proj.add(projetil)
        disparar.play()
        
    def move(self, vel): # Lida com o movimento do player na tela
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left - vel > -60:
            self.rect.x -= vel
        if keys[pygame.K_RIGHT] and self.rect.right + vel < largura + 60:
            self.rect.x += vel
        if keys[pygame.K_UP] and self.rect.top - vel > 0:
            self.rect.y -= vel
        if keys[pygame.K_DOWN] and self.rect.bottom + vel < altura:
            self.rect.y += vel

    def update(self):
        self.proj.update()

# Inimigo
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, img, hp=1, vel_y=None):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = hp
        self.vel_y = vel_y if vel_y is not None else 3  # Enquanto o chefe não spawnar, utiliza a velocidade padrão dos inimigos

    def move(self, vel):
        self.rect.y += self.vel_y  # Velocidade de descida dos inimigos
    # Define uma pos. nova aleatória para o inimigo
    def respawn(self, largura):
        self.rect.x = random.randint(0, largura - self.rect.width) # Define pos. horizontal
        self.rect.y = random.randint(-150, -self.rect.height) # Define pos. vertical
    
    def dano(self):
        dano_chefe.play()
        self.hp -= 1 # Reduz HP do inimigo em 1
        if self.hp <= 0:
            self.kill() # Quando o HP chega a zero remove o inimigo da tela

# |||||||||||||||||||||| INICIANDO MAIN() LOOP ||||||||||||||||||||||||||||||||||
def main():
    rodando = True
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("Segoe UI Emoji", 30) # Seleção e tamanho de fonte
    vel_player = 12   # Velocidade de movimento do sprite do player
    vel_y_inimigo = 3 # Velocidade de movimento do sprite do Inimigo
    vel_y_chefe = 1 # Velocidade de movimento do sprite do Chefe 
    inimigos = pygame.sprite.Group() # Cria um grupo para adicionar os inimigos
    score = 0 # Quantos cães o player vacinou
    boss_spawnado = False # Checa se o chefe não spawnou ainda
    
    # Adc movimento ao background
    global bg_y # Declara bg como global
    global scroll_speed # Controla a vel. do bg
    bg_y = 0
    scroll_speed = 2

    carro = Player(105, 520)  # pos. do player em relação a tela
    
    pygame.mixer.music.load(os.path.join("SFX", "Loop_TreasureHunter_02.mp3"))
    pygame.mixer.music.play(-1) 

    # Spawnando inimigos ao topo do mapa em posições aleatórias
    for _ in range(2):  # Criar 2 Inimigos 
        inimigo1 = Inimigo(random.randint(0, largura - 100), random.randint(-150, -100), dog1) 
        inimigo2 = Inimigo(random.randint(0, largura - 100), random.randint(-150, -100), dog2)
        inimigo3 = Inimigo(random.randint(0, largura - 100), random.randint(-150, -100), dog3)
        inimigos.add(inimigo1, inimigo2, inimigo3) # Adc inimigos a variável 'inimigos'

    # Chefão
    def spawn_chefe():
        global boss
        # Tema do chefe
        pygame.mixer.music.load(os.path.join("SFX", "Loop_Run_For_Your_Life_03.mp3"))
        pygame.mixer.music.play(-1) 
        inimigos.empty()
        boss_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "chefe.png")), (150, 150))  
        boss_width = boss_img.get_width()  
        boss_height = boss_img.get_height() 
        boss_x = (largura - boss_width) // 2 
        boss_y = -boss_height
        boss = Inimigo(boss_x, boss_y, boss_img, hp=120, vel_y=vel_y_chefe)  # Chefe herda as variáveis da 'class' Inimigo
        inimigos.add(boss) # Adc o chefe ao grupo 'inimigos'
    
    # Desenha na tela os elementos 'bg', 'vidas', e HP do Chefe
    def display_redraw():
        # Desenha o movimento do bg
        global bg_y
        global scroll_speed
        bg_y += scroll_speed
        if bg_y > altura:
            bg_y = 0
        display.blit(bg, (0, bg_y))
        display.blit(bg, (0, bg_y - altura))
        
        display_vidas = fonte.render(f"\u2764{carro.vidas}", True, (255, 0, 0))  # Renderiza o nome "Vidas" junto a sua respectiva variável
        display.blit(display_vidas, (10, 10))  # pos. onde display_vidas será mostrado na tela
        display_score = fonte.render(f'Score: {score}/100', True, (255, 255, 255))
        display.blit(display_score, (10, 50))  # Mostra o score na tela
        

        
        if boss_spawnado:
            boss_hp_text = fonte.render(f'Cãopeta\u2764: {boss.hp}', True, (255, 0, 0))  # Red color for boss health
            display.blit(boss_hp_text, (10, 90))  # Pos. onde o hp do chefe será mostrado na tela
    
        carro.draw(display)
        inimigos.draw(display)

        pygame.display.update()
        
    # Tela de vitória
    def game_won():
        inimigos.empty()
        pygame.mixer.music.load(os.path.join("SFX", "Jingle_Win_00.mp3"))
        pygame.mixer.music.play()
        fonte = pygame.font.SysFont("Segoe UI Bold", 25)
        display_vitoria = fonte.render('Você ganhou! [ESPAÇO] P/ Voltar ao MENU', 1, (255, 255, 0))
        texto_vitoria = display_vitoria.get_rect(center=(largura / 2, altura / 2))
        display.blit(display_vitoria, texto_vitoria)
        pygame.display.update()

        # Timer da tela de vitória
        pygame.time.wait(2000)  # Aguarda 2 Segundos (ms)
        
        # Espera o input do usuário
        aguardando = True
        while aguardando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        aguardando = False
                        pygame.quit()
                        subprocess.run(["python", "py_jogoMenu.py"]) # Retorna ao menu principal
                        sys.exit()

    # Leva o player devolta para o menu principal
    def game_over():
        inimigos.empty()
        pygame.mixer.music.load(os.path.join("SFX", "Jingle_Lose_00.mp3"))
        pygame.mixer.music.play()
        fonte = pygame.font.SysFont("Segoe UI Bold", 25)
        display_vitoria = fonte.render('Você Perdeu! [ESPAÇO] P/ Voltar ao MENU', 1, (255, 0, 0))
        texto_vitoria = display_vitoria.get_rect(center=(largura / 2, altura / 2))
        display.blit(display_vitoria, texto_vitoria)
        pygame.display.update()

        # Timer da tela de derrota
        pygame.time.wait(2000)  # Aguarda 2 Segundos (ms)
        
        # Espera o input do usuário
        aguardando = True
        while aguardando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        aguardando = False
                        pygame.quit()
                        subprocess.run(["python", "py_jogoMenu.py"]) # Retorna ao menu principal
                        sys.exit()

    # ||||||||||||||||||||||||||||| RESPONSÁVEL POR RODAR OS ASPECTOS PRINCIPAIS DO JOGO |||||||||||||||||||||||||||||||||||||||||||||||||||
    while rodando:
        relogio.tick(60)  # Framerate
        display_redraw() # Atualiza a tela

        carro.move(vel_player) # Move o player com base na vel.
        carro.update() # Atualiza o estado dos projéteis
        
        if score == 99 and not boss_spawnado: # Checa se o score é igual 99 e se o boss_spawnando é False
            spawn_chefe()
            boss_spawnado = True

        for inimigo in inimigos:
            inimigo.move(vel_y_inimigo)

            if not boss_spawnado: # Se o inimigo sair da tela o player perde vida
                if inimigo.rect.top > altura:
                    carro.vidas -= 1
                    dano_player.play()
                    inimigo.respawn(largura) # Inimigo respawna no topo da tela
                    if carro.vidas <= 0:
                        game_over()

            if pygame.sprite.collide_mask(carro, inimigo):
                carro.vidas -= 1
                dano_player.play()
                inimigo.respawn(largura)
                if carro.vidas <= 0:
                    game_over()

            # CHECA COLISÕES ENTRE PROJÉTEIS DO PLAYER, INIMIGO E O CHEFE
            if pygame.sprite.spritecollide(inimigo, carro.proj, True, pygame.sprite.collide_mask):
                if boss_spawnado and inimigo == boss:
                    inimigo.dano() # Reduz HP do chefe
                    if boss.hp <= 0:
                        morte_chefe.play()
                        if score < 99:
                            score += 1  
                        inimigo.kill()  # Remove o chefe da tela
                        pygame.display.update()
                        pygame.time.wait(200)  # Espera para mostrar a vitória
                        game_won()  # Garante que o jogo é encerrado corretamente
                else:
                    morte_inimigo.play()
                    score += 1
                    inimigo.respawn(largura)
                    
        # Se o chefe sair da tela, mata o player automaticamente
        if boss_spawnado and boss.rect.top > altura:
            carro.vidas = 0
            dano_player.play()
            pygame.display.update()
            pygame.time.wait(200)
            game_over()

        # FIM DO CHEQUE DE CONLISÕES
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False # Sai do loop e fecha a janela
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    carro.disparar() # Dispara um projétil ao pressioanr ESPAÇO

    # |||||||||||||||||||||||FIM DO WHILE LOOP|||||||||||||||||||||||||||||
# |||||||||||||||||||||||||||FIM DO MAIN() LOOP|||||||||||||||||||||||||||||

# Menu antes de iniciar o jogo
def iniciar():
    titulo_fonte = pygame.font.SysFont("Segoe UI Bold", 32) # Define a fonte + tamanho
    tela_largura, tela_altura = largura, altura
    rodando = True
    while rodando:
        display.blit(bg, (0,0)) # Renderiza o fundo
        iniciar_titulo = titulo_fonte.render("Aperte [ESPAÇO] para começar", True, (255,255,255))
        text_rect = iniciar_titulo.get_rect(center=(tela_largura / 2, tela_altura / 2)) # Centraliza o texto na tela
        display.blit(iniciar_titulo, text_rect.topleft) # Desenha o texto na tela
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main() # Inicia o jogo 
    pygame.quit()

iniciar()


