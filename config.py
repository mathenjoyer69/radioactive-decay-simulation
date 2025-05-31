import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atom Decay Simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
BLUE = (65, 105, 225)
RED = (255, 0, 0)
purple = (100, 50, 150)
dark_purple = (70, 20, 100)
green = (50, 150, 50)
dark_green = (20, 100, 20)
green_button = (50, 200, 50)
dark_green_button = (20, 150, 20)
gray = (100, 100, 100)
dark_gray = (70, 70, 70)

font = pygame.font.SysFont(None, 24)
small_font = pygame.font.SysFont(None, 20)

isotopes = {
    "polonium": {
        "symbol": "Po-210",
        "half_life": 138.376 * 365.25,
        "decay_product": "Pb-206",
        "color": (139, 0, 255),
        "decay_product_color": (70, 130, 180)
    },
    "rubidium": {
        "symbol": "Rb-87",
        "half_life": 48.8e9 * 365.25,
        "decay_product": "Sr-87",
        "color": (255, 69, 0),
        "decay_product_color": (0, 191, 255)
    }
}