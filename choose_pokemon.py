import pygame
import requests
from io import BytesIO
import json

class ChoosePokemon:
    def __init__(self, window):
        self.window = window
        self.pokemon_choices = ["charmander", "squirtle", "bulbasaur"]
        self.pokemon_sprites = {}
        self.load_pokemon_sprites()
        self.selected_pokemon = None
        self.font = pygame.font.Font("freesansbold.ttf", 20)  # Réduire la taille de la police
        self.hovered_pokemon = None
        self.button_color = (79, 109, 224)
        self.hover_color = (104, 129, 224)
        self.text_color = (255, 255, 255)
        self.pokemon_rects = []

    def load_pokemon_sprites(self):
        for pokemon_name in self.pokemon_choices:
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    sprite_url = data['sprites']['front_default']
                    sprite_response = requests.get(sprite_url)
                    if sprite_response.status_code == 200:
                        sprite_image = pygame.image.load(BytesIO(sprite_response.content))
                        sprite_image = pygame.transform.scale(sprite_image, (120, 120))
                        self.pokemon_sprites[pokemon_name] = sprite_image
                    else:
                        print(f"Erreur de chargement du sprite pour {pokemon_name}")
                else:
                    print(f"Erreur: Impossible de récupérer les données du Pokémon {pokemon_name}")
            except requests.exceptions.RequestException as e:
                print(f"Erreur de connexion: {e}")

    def mark_pokemon_as_captured(self, pokemon_name):
        """Marque un Pokémon comme capturé dans le fichier JSON."""
        try:
            with open("pokemon_data.json", "r") as file:
                pokemon_data = json.load(file)
            
            for pokemon in pokemon_data["pokemons"]:
                if pokemon["name"] == pokemon_name:
                    pokemon["captured"] = True
                    break
            
            with open("pokemon_data.json", "w") as file:
                json.dump(pokemon_data, file, indent=4)
        except Exception as e:
            print(f"Erreur lors de la mise à jour du fichier JSON : {e}")

    def display_choices(self):
        self.window.screen_surface.fill((0, 0, 0))  # Fond noir

        title_text = self.font.render("Choisissez votre Pokémon :", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.window.longueur // 2, 50))
        self.window.screen_surface.blit(title_text, title_rect)

        x_offset = self.window.longueur // 4
        y_offset = 200
        self.pokemon_rects = []

        for pokemon_name in self.pokemon_choices:
            sprite = self.pokemon_sprites.get(pokemon_name)
            if sprite:
                pokemon_rect = sprite.get_rect(center=(x_offset, y_offset))
                self.pokemon_rects.append((pokemon_name, pokemon_rect))

                current_color = self.hover_color if self.hovered_pokemon == pokemon_name else self.button_color

                pygame.draw.rect(self.window.screen_surface, current_color, pokemon_rect.inflate(20, 20), border_radius=10)

                sprite_rect = sprite.get_rect(center=(x_offset, y_offset - 10))
                self.window.screen_surface.blit(sprite, sprite_rect)

                name_text = self.font.render(pokemon_name.capitalize(), True, self.text_color)
                name_rect = name_text.get_rect(center=(x_offset, y_offset + 90))  # Ajuster la position verticale du texte
                self.window.screen_surface.blit(name_text, name_rect)

                x_offset += self.window.longueur // 4

    def events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_pokemon = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False
            elif event.type == pygame.MOUSEMOTION:
                for pokemon_name, pokemon_rect in self.pokemon_rects:
                    if pokemon_rect.collidepoint(mouse_pos):
                        self.hovered_pokemon = pokemon_name
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for pokemon_name, pokemon_rect in self.pokemon_rects:
                    if pokemon_rect.collidepoint(mouse_pos):
                        self.selected_pokemon = pokemon_name
                        self.mark_pokemon_as_captured(pokemon_name)  # Marquer le Pokémon comme capturé
                        self.start_fight()
                        break

    def start_fight(self):
        if self.selected_pokemon:
            from game import Fight
            fight_screen = Fight(self.window, self.selected_pokemon)
            fight_screen.run_game()

    def run_game(self):
        while self.window.running:
            self.events()
            self.display_choices()
            self.window.update_display()