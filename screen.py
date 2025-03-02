import pygame 
import requests # J'importe une bibliothèque
from io import BytesIO # Permet de lié les données de la bibliothèque
import os
from game import Fight # J'importe ma fonction Fight de ma page game
from pokedex import Pokedex # J'importe ma fontion Pokedex de ma page pokedex
from choose_pokemon import ChoosePokemon # J'importe ma fonction ChoosePokemon de ma page choose_pokemon

pygame.init()

class Screen: # Je créer une première classe pour ma fenetre
    def __init__(self, longueur=900, largeur=600):
        self.longueur = longueur
        self.largeur = largeur
        self.screen_surface = pygame.display.set_mode((self.longueur, self.largeur))
        pygame.display.set_caption("PokémonGame")
        self.running = True

    def update_display(self):
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run_game(self):
        while self.running:
            self.events()
            self.update_display()

class Home(Screen): # Je créer cette classe qui hérite de Screen pour conserver son constructeur, cette classe servira pour le contenu de la fenetre 
    def __init__(self):
        super().__init__()

        if os.path.exists('pokebk.png'):
            self.background = pygame.transform.scale(pygame.image.load('pokebk.png'), (900, 600))
        else:
            self.background = None

        if os.path.exists('Bienvenue.png'):
            self.title_image = pygame.image.load('Bienvenue.png')
            self.title_image = pygame.transform.scale(self.title_image, (600, 150))

        self.font_buttons = pygame.font.Font("freesansbold.ttf", 30)

        self.button_color = (30, 144, 255) 
        self.button_hover_color = (0, 191, 255)  
        self.button_text_color = (255, 255, 255)  

        self.buttons = [
            {"rect": pygame.Rect(100, 200, 300, 60), "text": "Nouvelle partie", "action": self.new_game},
            {"rect": pygame.Rect(80, 340, 340, 60), "text": "Accéder au Pokédex", "action": self.show_pokedex}
        ]

    def menu(self):

        self.screen_surface.blit(self.background, (0, 0))

        title_x = (self.longueur - self.title_image.get_width()) // 2 
        title_y = 0  
        self.screen_surface.blit(self.title_image, (title_x, title_y))

        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            rect = button["rect"]

            color = self.button_hover_color if rect.collidepoint(mouse_pos) else self.button_color
            pygame.draw.rect(self.screen_surface, color, rect, border_radius=10) 

            pygame.draw.rect(self.screen_surface, (0, 0, 0), rect, 3, border_radius=10)

            text = self.font_buttons.render(button["text"], True, self.button_text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen_surface.blit(text, text_rect)

    def new_game(self):# Cette fonction permet d'afficher le choix des pokemons et démarre l'écran de sélection 
        choose_pokemon_screen = ChoosePokemon(self)
        choose_pokemon_screen.run_game()

    def show_pokedex(self):# Cette fonction permet d'afficher les pokemons a choisir
        pokedex_screen = Pokedex(self)
        pokedex_screen.run_game()

# J'éxecute les evenements de la page
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["action"]()

# Je fais  une boucle principale pour éxecuter l'ensemble des méthodes utilisés
    def run_game(self):
        while self.running:
            self.menu()
            self.events()
            self.update_display()

if __name__ == "__main__":
    home_screen = Home()
    home_screen.run_game()