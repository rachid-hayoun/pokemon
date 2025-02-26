# windows.py

import pygame

# Initialisation de pygame
pygame.init()

class Windows:
    def __init__(self, longueur=900, largeur=600):
        self.longueur = longueur
        self.largeur = largeur
        self.screen = pygame.display.set_mode((self.longueur, self.largeur))
        pygame.display.set_caption("PokémonGame")

    def update_display(self):
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def run_game(self):
        self.running = True
        while self.running:
            self.running = self.events()
            self.update_display()

class Home(Windows):
    def __init__(self):
        super().__init__()

        self.background = pygame.transform.scale(pygame.image.load('pokebk.png'), (900, 600))
        self.font_m = pygame.font.Font("freesansbold.ttf", 26)
        self.text = self.font_m.render("Bienvenue sur mon Pokémon !", True, (0, 0, 0))

        self.font_button1 = pygame.font.Font("freesansbold.ttf", 26)
        self.text_button1 = self.font_button1.render("Nouvelle partie !", True, (255, 255, 255))
        self.font_button2 = pygame.font.Font("freesansbold.ttf", 26)
        self.text_button2 = self.font_button2.render("Ajouter un pokémon", True, (255, 255, 255))
        self.font_button3 = pygame.font.Font("freesansbold.ttf", 26)
        self.text_button3 = self.font_button3.render("Accéder au Pokédex", True, (255, 255, 255))

        self.button_rect1 = pygame.Rect(80, 200, 280, 50)
        self.button_rect2 = pygame.Rect(80, 300, 280, 50)
        self.button_rect3 = pygame.Rect(80, 400, 280, 50)

        self.running = True
        self.state = "menu"

    def menu(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.text, (40, 90))
        pygame.draw.rect(self.screen, (0, 128, 0), self.button_rect1)
        pygame.draw.rect(self.screen, (0, 128, 0), self.button_rect2)
        pygame.draw.rect(self.screen, (0, 128, 0), self.button_rect3)
        self.screen.blit(self.text_button1, (self.button_rect1.x + 35, self.button_rect1.y + 10))
        self.screen.blit(self.text_button2, (self.button_rect2.x + 15, self.button_rect2.y + 10))
        self.screen.blit(self.text_button3, (self.button_rect3.x + 15, self.button_rect3.y + 10))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect1.collidepoint(event.pos):  
                    self.state = "new_game"
                elif self.button_rect2.collidepoint(event.pos):  
                    print("Ajouter un pokémon")
                elif self.button_rect3.collidepoint(event.pos): 
                    print("Accéder au Pokédex")

    def run_game(self):
        while self.running:
            if self.state == "menu":
                self.menu()
            elif self.state == "new_game":
                new_game_screen = NewGame(self)  # Créer une instance de NewGame
                new_game_screen.run_game()  # Lancer la nouvelle partie
                self.state = "menu"
            self.events()
            self.update_display()
            
class NewGame(Windows):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.running = True

    def game(self):
        self.screen.fill((255, 255, 255))  # Fond blanc
        font = pygame.font.Font("freesansbold.ttf", 40)
        text = font.render("Choisissez votre pokémon", True, (0, 0, 0))
        self.screen.blit(text, (300, 250))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.running = False  # Ferme la fenêtre de la nouvelle partie

    def run_game(self):
        while self.running:
            self.game()
            self.events()
            self.update_display()
        self.parent_window.state = "menu"  # Retour au menu après la fin du jeu
