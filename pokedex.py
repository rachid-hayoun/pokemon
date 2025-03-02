import pygame
import requests
from io import BytesIO
import os
import json

class Pokedex:
    def __init__(self, window):
        self.window = window
        self.pokemon_list = []
        self.load_captured_pokemon() 
        self.items_per_page = 9  
        self.current_page = 0
       
        self.button_color = (30, 144, 255)  
        self.button_hover_color = (0, 191, 255)  
        self.button_text_color = (255, 255, 255) 

    def load_captured_pokemon(self):
        """Charge les Pokémon capturés depuis le fichier JSON."""
        with open("pokemon_data.json", "r") as file:
            pokemon_data = json.load(file)
            for pokemon in pokemon_data["pokemons"]:
                if pokemon.get("captured", False):  
                    self.fetch_pokemon_data(pokemon["name"])

    def fetch_pokemon_data(self, pokemon_name):
        """Récupère les données d'un Pokémon depuis l'API."""
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                pokemon_name = data['name']
                pokemon_sprite_url = data['sprites']['front_default']
                sprite_response = requests.get(pokemon_sprite_url)
                if sprite_response.status_code == 200:
                    sprite_image = pygame.image.load(BytesIO(sprite_response.content))
                    sprite_image = pygame.transform.scale(sprite_image, (80, 80))
                    self.pokemon_list.append({'name': pokemon_name, 'sprite': sprite_image})
                else:
                    print(f"Erreur: Impossible de télécharger le sprite de {pokemon_name}")
            else:
                print(f"Erreur: Impossible de récupérer les données du Pokémon {pokemon_name}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion pour {pokemon_name}: {e}")

    def display_pokedex(self):
        background_path = "pokedex.png"
        if os.path.exists(background_path):
            background = pygame.image.load(background_path)
            background = pygame.transform.scale(background, (self.window.longueur, self.window.largeur))
            self.window.screen_surface.blit(background, (0, 0))
        else:
            self.window.screen_surface.fill((255, 255, 255))

        font = pygame.font.Font("freesansbold.ttf", 40)
        text = font.render("Pokédex", True, (0, 0, 0))
        self.window.screen_surface.blit(text, (350, 50))

        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page

        pokemon_to_display = self.pokemon_list[start_index:end_index]

        x_offset = 80
        y_offset = 150
        index = 0

        for pokemon in pokemon_to_display:
            x = x_offset + (index % 3) * 200
            y = y_offset + (index // 3) * 150

            self.window.screen_surface.blit(pokemon['sprite'], (x, y))

            name_font = pygame.font.Font("freesansbold.ttf", 20)
            name_text = name_font.render(pokemon['name'].capitalize(), True, (0, 0, 0))
            name_rect = name_text.get_rect(center=(x + 40, y + 95))
            self.window.screen_surface.blit(name_text, name_rect)

            index += 1

        self.display_navigation_buttons()

    def display_navigation_buttons(self):
        font = pygame.font.Font("freesansbold.ttf", 24)
        prev_button_rect = pygame.Rect(50, 100, 170, 30)
        next_button_rect = pygame.Rect(700, 100, 170, 30)

        # Effet de survol
        mouse_pos = pygame.mouse.get_pos()
        prev_color = self.button_hover_color if prev_button_rect.collidepoint(mouse_pos) else self.button_color
        next_color = self.button_hover_color if next_button_rect.collidepoint(mouse_pos) else self.button_color

        # Bouton Précédent
        pygame.draw.rect(self.window.screen_surface, prev_color, prev_button_rect, border_radius=10)
        pygame.draw.rect(self.window.screen_surface, (0, 0, 0), prev_button_rect, 3, border_radius=10)
        prev_text = font.render("Précédent", True, self.button_text_color)
        prev_text_rect = prev_text.get_rect(center=prev_button_rect.center)
        self.window.screen_surface.blit(prev_text, prev_text_rect)

        # Bouton Suivant
        pygame.draw.rect(self.window.screen_surface, next_color, next_button_rect, border_radius=10)
        pygame.draw.rect(self.window.screen_surface, (0, 0, 0), next_button_rect, 3, border_radius=10)
        next_text = font.render("Suivant", True, self.button_text_color)
        next_text_rect = next_text.get_rect(center=next_button_rect.center)
        self.window.screen_surface.blit(next_text, next_text_rect)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.Rect(50, 100, 120, 30).collidepoint(event.pos):
                        self.current_page = max(0, self.current_page - 1)
                    elif pygame.Rect(750, 100, 100, 30).collidepoint(event.pos):
                        max_page = (len(self.pokemon_list) - 1) // self.items_per_page
                        self.current_page = min(max_page, self.current_page + 1)

    def run_game(self):
        while self.window.running:
            self.display_pokedex()
            self.events()
            self.window.update_display()