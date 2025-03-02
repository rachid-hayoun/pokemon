import pygame
import requests
from io import BytesIO
import random
import os
import json # J'importe le module json de la bibliothèque

pygame.init()

# Je place ici mes constantes 
MAX_HEALTH = 100 # Point de vie max
CHARGE_DAMAGE = 10 # Dégats causés par Charge
VIVE_ATTAQUE_DAMAGE = 20 # Dégats causés par Vive-attaque
BUTTON_COLOR = (79, 109, 224) # Couleur du bouton
BUTTON_HOVER_COLOR = (104, 129, 224) # Couleur de l'effet de survol
BUTTON_TEXT_COLOR = (255, 255, 255) # Couleur du texte du bouton
ATTACK_SPEED = 8 # Vitesse d'attaque du Pokemon
ATTACK_DURATION = 30  # Durée de l'animation de l'attaque
RETURN_DURATION = 20  # Durée du retour du pokémon

class Fight: # Je créer une classe pour le combat avec un pokemon choisi et un pokemon adversaire aléatoire
    def __init__(self, window, player_pokemon=None):
        self.window = window
        self.player_pokemon = player_pokemon
        self.pokemon_data = self.load_pokemon_data()  
        self.opponent_pokemon = self.get_random_pokemon()  
        self.font = pygame.font.Font("freesansbold.ttf", 20)

# Positiion de mon pokemon et du pokemon adverse ainsi que les points de vie et le niveau
        self.player_data = self.fetch_pokemon_data(self.player_pokemon)
        self.player_health = MAX_HEALTH
        self.player_level = 1
        self.player_attacking = False
        self.player_start_pos = (100, 350)
        self.player_attack_pos = (550, 150)  
        self.player_current_pos = self.player_start_pos
        self.attack_frame = 0
        self.returning = False 

# Information du pokemon adverse
        self.opponent_data = self.fetch_pokemon_data(self.opponent_pokemon)
        self.opponent_health = MAX_HEALTH
        self.opponent_level = 1

        self.background = pygame.transform.scale(pygame.image.load('fight.png'), (window.longueur, window.largeur))

        self.game_over = False
        self.attack_available = True
        # Button d'attaque
        self.buttons = [
            {"rect": pygame.Rect(650, 450, 150, 40), "text": "Charge", "action": self.use_charge},
            {"rect": pygame.Rect(650, 500, 150, 40), "text": "Vive-Attaque", "action": self.use_vive_attaque}
        ]
        self.hovered_button = None
        self.current_damage = 0  

    def load_pokemon_data(self):
        """Charge les données des Pokémon depuis le fichier JSON."""
        with open("pokemon_data.json", "r") as file:
            return json.load(file)

    def get_random_pokemon(self):
        """Sélectionne un Pokémon aléatoire depuis le fichier JSON."""
        pokemon_list = self.pokemon_data["pokemons"]
        return random.choice(pokemon_list)["name"]

    def fetch_pokemon_data(self, pokemon_name):
        """Récupère les données d'un Pokémon depuis l'API."""
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                sprite_url = data['sprites']['front_default']
                sprite_response = requests.get(sprite_url)
                if sprite_response.status_code == 200:
                    sprite_image = pygame.image.load(BytesIO(sprite_response.content))
                    sprite_image = pygame.transform.scale(sprite_image, (170, 170))
                    return {'name': data['name'], 'sprite': sprite_image, 'data': data}
                else:
                    print(f"Erreur de chargement du sprite pour {pokemon_name}")
                    return None
            else:
                print(f"Erreur: Impossible de récupérer les données du Pokémon {pokemon_name}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion: {e}")
            return None

    def use_charge(self):
        if self.player_data and self.opponent_data and not self.game_over and self.attack_available:
            self.start_attack(CHARGE_DAMAGE)

    def use_vive_attaque(self):
        if self.player_data and self.opponent_data and not self.game_over and self.attack_available:
            self.start_attack(VIVE_ATTAQUE_DAMAGE)

    def start_attack(self, damage):
        self.player_attacking = True
        self.attack_frame = 0
        self.returning = False
        self.attack_available = False
        self.current_damage = damage
        print(f"Le joueur utilise une attaque qui inflige {damage} dégâts!")

    def check_winner(self):
        if self.player_health <= 0:
            self.winner = "L'adversaire"
            self.game_over = True
        elif self.opponent_health <= 0:
            self.winner = "Le joueur"
            self.game_over = True
            # Marquer le Pokémon adverse comme capturé
            self.mark_pokemon_as_captured(self.opponent_data['name'])

    def mark_pokemon_as_captured(self, pokemon_name):
        """Marque un Pokémon comme capturé dans le fichier JSON."""
        for pokemon in self.pokemon_data["pokemons"]:
            if pokemon["name"] == pokemon_name:
                pokemon["captured"] = True
                break
        # Sauvegarder les modifications dans le fichier JSON
        with open("pokemon_data.json", "w") as file:
            json.dump(self.pokemon_data, file, indent=4)

    def apply_damage(self):
        self.opponent_health -= self.current_damage
        if self.opponent_health < 0:
            self.opponent_health = 0
        print(f"L'adversaire perd {self.current_damage} PV. PV restant : {self.opponent_health}")

    def display_fight(self):
        if self.background:
            self.window.screen_surface.blit(self.background, (0, 0))
        else:
            self.window.screen_surface.fill((255, 255, 255))

        if self.player_data and self.opponent_data:
            if self.player_attacking:
                if self.attack_frame < ATTACK_DURATION:
                    ratio = self.attack_frame / ATTACK_DURATION
                    distance_x = (self.player_attack_pos[0] - self.player_start_pos[0]) * ratio
                    distance_y = (self.player_attack_pos[1] - self.player_start_pos[1]) * ratio
                    self.player_current_pos = (self.player_start_pos[0] + distance_x, self.player_start_pos[1] + distance_y)
                elif self.returning and self.attack_frame < ATTACK_DURATION + RETURN_DURATION:
                    return_ratio = (self.attack_frame - ATTACK_DURATION) / RETURN_DURATION
                    return_distance_x = (self.player_start_pos[0] - self.player_attack_pos[0]) * return_ratio
                    return_distance_y = (self.player_start_pos[1] - self.player_attack_pos[1]) * return_ratio
                    self.player_current_pos = (self.player_attack_pos[0] + return_distance_x, self.player_attack_pos[1] + return_distance_y)
                else:
                    self.player_current_pos = self.player_start_pos

            self.window.screen_surface.blit(self.player_data['sprite'], self.player_current_pos)
            text_player = self.font.render(f"{self.player_data['name'].capitalize()} (Niv. {self.player_level})", True, (255, 255, 255))
            self.window.screen_surface.blit(text_player, (100, 320))
            self.draw_health_bar(100, 345, self.player_health, MAX_HEALTH, (0, 255, 0))

            self.window.screen_surface.blit(self.opponent_data['sprite'], (550, 150))
            text_opponent = self.font.render(f"{self.opponent_data['name'].capitalize()} (Niv. {self.opponent_level})", True, (255, 255, 255))
            self.window.screen_surface.blit(text_opponent, (550, 120))
            self.draw_health_bar(550, 145, self.opponent_health, MAX_HEALTH, (255, 0, 0))

            if not self.game_over:
                for button in self.buttons:
                    rect = button["rect"]
                    current_color = BUTTON_HOVER_COLOR if self.hovered_button == button else BUTTON_COLOR
                    pygame.draw.rect(self.window.screen_surface, current_color, rect)
                    text_surface = self.font.render(button["text"], True, BUTTON_TEXT_COLOR)
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.window.screen_surface.blit(text_surface, text_rect)

            else:
                winner_text = self.font.render(f"Vainqueur: {self.winner}!", True, (255, 255, 255))
                winner_rect = winner_text.get_rect(center=(self.window.longueur // 2, 50))
                self.window.screen_surface.blit(winner_text, winner_rect)

        pygame.display.flip()

    def draw_health_bar(self, x, y, health, max_health, color):
        bar_width = 150
        bar_height = 10
        health_ratio = health / max_health
        pygame.draw.rect(self.window.screen_surface, (255, 255, 255), (x, y, bar_width, bar_height))
        pygame.draw.rect(self.window.screen_surface, color, (x, y, bar_width * health_ratio, bar_height))

    def events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_button = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False
            elif event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        self.hovered_button = button
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos) and self.attack_available:
                        self.hovered_button = button
                        button["action"]()
                        break

    def run_game(self):
        clock = pygame.time.Clock()
        while self.window.running:
            self.events()
            if self.player_attacking:
                self.attack_frame += 1
                if self.attack_frame == ATTACK_DURATION:
                    self.apply_damage()
                    self.returning = True 
                elif self.attack_frame >= ATTACK_DURATION + RETURN_DURATION:
                    self.player_attacking = False
                    self.attack_available = True
                    self.returning = False
                    self.attack_frame = 0
                    self.check_winner()

            self.display_fight()
            pygame.display.flip()
            clock.tick(60)