import sys
import math
import random

from avion import Avion

MIN_SPEED_KM_S = 0.16
MAX_SPEED_KM_S = 0.31

class EspaceAerien:
    def __init__(self, rayon_km):
        self.liste_avions = []
        self.rayon = rayon_km

        for i in range(3):
            self.add_random_avion(f"RND{i + 1:02}")

    def add_random_avion(self, id_vol):
        """Génère un nouvel avion avec des paramètres aléatoires dans la zone de radar."""


        r = self.rayon * random.uniform(0.1, 1.0)
        theta = random.uniform(0, 2 * math.pi)

        x = r * math.cos(theta)
        y = r * math.sin(theta)


        cap_deg = random.randint(0, 359)


        vitesse_km_s = random.uniform(MIN_SPEED_KM_S, MAX_SPEED_KM_S)

        avion = Avion(id_vol, x, y, cap_deg, vitesse_km_s)
        self.liste_avions.append(avion)
        print(
            f"Nouveau avion spawn: {avion.id_vol} à ({x:.1f}, {y:.1f}), Cap {cap_deg}°, Vitesse {vitesse_km_s:.2f} km/s.")

    def avion_en_plus(self, avion):
        self.liste_avions.append(avion)

    def update_positions(self, delta_t_s):
        """Déplace tous les avions et gère le remplacement des avions sortis de zone."""
        avions_a_garder = []

        for avion in self.liste_avions:
            avion.move(delta_t_s)


            distance_au_centre = math.sqrt(avion.x ** 2 + avion.y ** 2)

            if distance_au_centre <= self.rayon:
                avions_a_garder.append(avion)
            else:
                print(f"Avion {avion.id_vol} sorti de la zone à ({avion.x:.1f}, {avion.y:.1f}). Remplacement.")


        self.liste_avions = avions_a_garder


        avions_remplacés = 3 - len(self.liste_avions)
        for i in range(avions_remplacés):

            self.add_random_avion(f"NEW{random.randint(100, 999)}")