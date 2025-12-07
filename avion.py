import math
import random

ALTITUDES_POSSIBLES = [7000, 8000, 9000, 10000, 11000]


class Avion:
    def __init__(self, id_vol, x, y, cap_deg, vitesse_km_s, est_en_urgence=False, est_selectionne=False):
        self.id_vol = id_vol
        self.x = x
        self.y = y
        self.cap_deg = int(cap_deg)
        self.vitesse_km_s = vitesse_km_s
        self.est_en_urgence = est_en_urgence
        self.est_selectionne = est_selectionne

        self.altitude = random.choice(ALTITUDES_POSSIBLES)
        self.carburant = random.uniform(10.0, 70.0)

        # --- Variables pour l'atterrissage ---
        self.en_atterrissage = False
        self.target_x = 0
        self.target_y = 0
        self.altitude_depart_atterrissage = 0
        self.dist_totale_atterrissage = 0

    def entamer_atterrissage(self, cible_x, cible_y):
        """Active le mode atterrissage vers le point donné."""
        self.en_atterrissage = True
        self.target_x = cible_x
        self.target_y = cible_y
        self.altitude_depart_atterrissage = self.altitude

        # On mémorise la distance totale à parcourir au moment du clic
        self.dist_totale_atterrissage = math.sqrt((self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2)
        if self.dist_totale_atterrissage == 0: self.dist_totale_atterrissage = 1  # Eviter division par zero

    def move(self, delta_t_s):
        if self.en_atterrissage:
            # --- MODE ATTERRISSAGE ---
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist_restante = math.sqrt(dx ** 2 + dy ** 2)

            # Si on est très proche (< déplacement d'une frame), on considère qu'on est arrivé
            step_dist = self.vitesse_km_s * delta_t_s

            if dist_restante <= step_dist:
                self.x = self.target_x
                self.y = self.target_y
                self.altitude = 0
                return  # Arrivé sur la piste

            # Déplacement vers la cible
            angle_rad = math.atan2(dy, dx)  # Angle mathématique vers la cible
            self.x += step_dist * math.cos(angle_rad)
            self.y += step_dist * math.sin(angle_rad)

            # Mise à jour du cap visuel (pour que l'avion pointe vers la piste)
            # Conversion Math -> Nav : Nav = 90 - Math
            self.cap_deg = int((90 - math.degrees(angle_rad)) % 360)

            # Descente proportionnelle (Règle de 3)
            # Altitude = Altitude_Depart * (Distance_Restante / Distance_Totale)
            ratio = dist_restante / self.dist_totale_atterrissage
            self.altitude = int(self.altitude_depart_atterrissage * ratio)

        else:
            # --- MODE NORMAL ---
            cap_rad = math.radians(90 - self.cap_deg)
            distance = self.vitesse_km_s * delta_t_s

            self.x += distance * math.cos(cap_rad)
            self.y += distance * math.sin(cap_rad)

            # Conso carburant normale
            self.carburant -= (0.05 * self.vitesse_km_s)

        # Sécurité carburant
        if self.carburant < 0: self.carburant = 0

    def monter_palier(self):
        if self.en_atterrissage: return False  # Interdit de monter en atterrissage
        try:
            index_actuel = ALTITUDES_POSSIBLES.index(self.altitude)
            if index_actuel < len(ALTITUDES_POSSIBLES) - 1:
                self.altitude = ALTITUDES_POSSIBLES[index_actuel + 1]
                return True
        except ValueError:
            pass
        return False

    def descendre_palier(self):
        if self.en_atterrissage: return False
        try:
            index_actuel = ALTITUDES_POSSIBLES.index(self.altitude)
            if index_actuel > 0:
                self.altitude = ALTITUDES_POSSIBLES[index_actuel - 1]
                return True
        except ValueError:
            pass
        return False