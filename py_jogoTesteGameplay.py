import pygame
import sys

pygame.init()

largura = 800
altura = 600

branco = (255, 255, 255)
preto = (0, 0, 0)

screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("TESTE_JOGO")


def main_game():
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        screen.fill(preto)
        # Game logic goes here

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_game()
