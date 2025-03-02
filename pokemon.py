import pygame # J'importe pygame
from screen import Home # J'importe la classe Home de ma page screen

pygame.init()

pokemon_game = Home() 
pokemon_game.run_game()