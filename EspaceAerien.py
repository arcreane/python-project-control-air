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
            self.add_random_avion(f"START{i + 1}")

    def add_random_avion(self, id_vol):
        """Génère un nouvel avion SUR LE BORD avec un cap vers l'intérieur."""
        r = self.rayon
        theta = random.uniform(0, 2 * math.pi)

        x = r * math.cos(theta)
        y = r * math.sin(theta)

        angle_vers_centre = theta + math.pi
        variation = random.uniform(-math.pi / 4, math.pi / 4)
        angle_final_rad = angle_vers_centre + variation

        cap_deg = int((90 - math.degrees(angle_final_rad)) % 360)

        vitesse_km_s = random.uniform(MIN_SPEED_KM_S, MAX_SPEED_KM_S)

        avion = Avion(id_vol, x, y, cap_deg, vitesse_km_s)
        self.liste_avions.append(avion)
        print(f"Spawn: {avion.id_vol} bordure ({x:.1f}, {y:.1f}), Cap {cap_deg}°.")

    def update_positions(self, delta_t_s):
        """Déplace les avions, supprime ceux qui sortent et les remplace."""
        avions_a_garder = []
        nb_avions_sortis = 0

        for avion in self.liste_avions:
            avion.move(delta_t_s)

            distance_au_centre = math.sqrt(avion.x ** 2 + avion.y ** 2)
            marge_sortie = self.rayon + 0.1

            if distance_au_centre <= marge_sortie:
                avions_a_garder.append(avion)
            else:
                print(f"Sortie: {avion.id_vol} (Remplacement immédiat)")
                nb_avions_sortis += 1

        self.liste_avions = avions_a_garder

        for i in range(nb_avions_sortis):
            self.add_random_avion(f"RND{random.randint(100, 999)}")