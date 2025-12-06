import math
import random

# Les 5 niveaux de vol autorisés
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

    def move(self, delta_t_s):
        cap_rad = math.radians(90 - self.cap_deg)
        distance = self.vitesse_km_s * delta_t_s
        self.x += distance * math.cos(cap_rad)
        self.y += distance * math.sin(cap_rad)

    def monter_palier(self):
        """Essaie de monter au palier supérieur."""
        try:
            index_actuel = ALTITUDES_POSSIBLES.index(self.altitude)
            if index_actuel < len(ALTITUDES_POSSIBLES) - 1:
                self.altitude = ALTITUDES_POSSIBLES[index_actuel + 1]
                return True
        except ValueError:
            pass
        return False

    def descendre_palier(self):
        """Essaie de descendre au palier inférieur."""
        try:
            index_actuel = ALTITUDES_POSSIBLES.index(self.altitude)
            if index_actuel > 0:
                self.altitude = ALTITUDES_POSSIBLES[index_actuel - 1]
                return True
        except ValueError:
            pass
        return False