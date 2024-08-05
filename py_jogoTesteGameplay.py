# Importando libraries
import pygame
import os
import time
import random

pygame.init() # Iniciando Pygame
pygame.font.init()  # Iniciando fontes

# Tamanho da janela
largura, altura = 800, 600
display = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Campanha Antirábica") 

# Carregando Sprites
carro_img = pygame.transform.scale(pygame.image.load(os.path.join("PIXEL_ART", "carro0.png")), (200, 200))  # Player Sprite
dog1 = pygame.image.load(os.path.join("PIXEL_ART", "dog10.png"))  # Inimigo 01
dog2 = pygame.image.load(os.path.join("PIXEL_ART", "dog20.png"))  # Inimigo 02
vac = pygame.image.load(os.path.join("PIXEL_ART", "vacina0.png"))  # Projétil
bg = pygame.transform.scale(pygame.image.load(os.path.join("PIXEL_ART", "rua.png")), (largura, altura)) # Fundo COPYRIGHT: wwwdavidstenfors.com

# Player
class Player:
    def __init__(self, x, y, vida=1): # Definindo todas as variáveis que o jogador pode ter
        self.x = x
        self.y = y
        self.vida = vida
        self.player_img = carro_img
        self.player_vac = vac
        self.vac = [] 
        self.cd_cont = 0.5    
        self.mask = pygame.mask.from_surface(self.player_img)
    def draw(self, display):
        display.blit(self.player_img, (self.x, self.y))
        
# class Inimigo:
#   def __init__(self, x, y, vida=1):
#        self.x = x
#        self.y = y
#        self.vida = vida
#        self.
#        self.
#        self.cd_cont = 0.5    
#        self.mask = pygame.mask.from_surface()
#   def draw(self, display):
#       display.blit( , (self.x, self.y))
        
# Main loop
def main():
    rodando = True
    relogio = pygame.time.Clock() # Responsável por definir o framerate
    vidas = 3
    fonte = pygame.font.SysFont("Segoe UI Emoji", 30)
    vel_y = 5 # Velocidade de movimento do sprite do player
    
    carro = Player(0, 200) # Posição inicial do sprite do player

    def display_redraw():
        display.blit(bg, (0, 0)) # Renderiza o BG na tela
        display_vidas = fonte.render(f"\u2764{vidas}", 1, (255, 0, 0)) # Renderiza o nome Vidas junto a sua respectiva variável
        display.blit(display_vidas, (725, 10)) # pos. onde display_vidas sera mostrado na tela        
        carro.draw(display)

        pygame.display.update()

    while rodando:
        relogio.tick(60)
        display_redraw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
        
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_UP] and carro.y - vel_y > 0 - 100: 
            carro.y -= vel_y
        if tecla[pygame.K_DOWN] and carro.y + vel_y + carro.player_img.get_height() < altura + 50:
            carro.y += vel_y

main()
