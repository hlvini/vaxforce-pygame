import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
largura = 800
altura = 600

# Colors
branco = (255, 255, 255)
preto = (0, 0, 0)

# Create the display surface
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
