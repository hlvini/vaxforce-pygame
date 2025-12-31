import pygame # ce edition 
import sys
import subprocess
import os 

pygame.init()

# dimensões da janela
largura = 800
altura = 600

# cores do menu
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
VERDE = (0, 255, 0)

# Fontes
pygame.font.init()
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# superficie do display
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Inimigos da Raiva")

# carregando fundo
bg_image = pygame.image.load(os.path.join("assets", "bg_menu.jpeg"))
bg_image = pygame.transform.scale(bg_image, (largura, altura))

# efeitos sonoros
select = pygame.mixer.Sound(os.path.join("SFX", "Menu_Navigate_00.mp3"))

# menu
opcoes = ["[JOGAR]", "[CRÉDITOS]", "[SAIR]"]

def mostrar_creditos():
    while True:
        # Desenha imagem de fundo
        tela.blit(bg_image, (0, 0))

        # Desenha fundo preto semitransparente
        black_bg = pygame.Surface((largura, altura)) # Cria uma superfície do tamanho da tela
        black_bg.set_alpha(180) # Define a transparência (0-255, onde 255 é totalmente opaco)
        black_bg.fill((0, 0, 0)) # Preenche a superfície com preto
        tela.blit(black_bg, (0, 0)) # Desenha a superfície na tela

        # Desenha créditos
        credit_text = small_font.render("Créditos:", True, BRANCO)
        credit_rect = credit_text.get_rect(center=(largura // 2, 100))
        tela.blit(credit_text, credit_rect)

        credits = [
            "Desenvolvedor: por Hallen",
            "Música: por Little Robot Sound Factory",
            "Arte, BG do jogo: por Alucard",
        ]
        for i, line in enumerate(credits):
            text = small_font.render(line, True, AMARELO)
            text_rect = text.get_rect(center=(largura // 2, 150 + i * 40))
            tela.blit(text, text_rect)

        # Botão para voltar ao menu
        voltar_text = small_font.render("[VOLTAR]", True, VERDE)
        voltar_rect = voltar_text.get_rect(center=(largura // 2, altura - 50))
        tela.blit(voltar_text, voltar_rect)

        pygame.display.flip()  # Update do display

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Retorna ao menu

def menu():
    opcao_selec = 0
    pygame.mixer.music.load(os.path.join("SFX", "Loop_Someday_00.mp3"))
    pygame.mixer.music.play()
    while True:
        # Desenha imagem de fundo
        tela.blit(bg_image, (0, 0))

        # Desenha opções de menu
        for i, opcao in enumerate(opcoes):
            if i == opcao_selec:
                color = AMARELO
            else:
                color = BRANCO

            text = font.render(opcao, True, color)
            text_rect = text.get_rect(center=(largura // 2, 150 + i * 100))
            tela.blit(text, text_rect)

        pygame.display.flip()  # Update do display

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                select.play()
                if event.key == pygame.K_DOWN:
                    opcao_selec = (opcao_selec + 1) % len(opcoes)
                elif event.key == pygame.K_UP:
                    opcao_selec = (opcao_selec - 1) % len(opcoes)
                elif event.key == pygame.K_RETURN:
                    if opcao_selec == 0:
                        print("JOGAR")
                        pygame.quit()
                        subprocess.run(["python", "main.py"])
                        sys.exit()
                    elif opcao_selec == 1:
                        print("CRÉDITOS")
                        mostrar_creditos()
                    elif opcao_selec == 2:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    menu()
