import math

class Avion:
    def __init__(self, id_vol, x, y, cap_deg, vitesse_km_s, est_en_urgence=False, est_selectionne=False):
        self.id_vol = id_vol
        self.x = x
        self.y = y
        self.cap_deg = cap_deg
        self.vitesse_km_s = vitesse_km_s
        self.est_en_urgence = est_en_urgence
        self.est_selectionne = est_selectionne

    def move(self, delta_t_s):

        cap_rad = math.radians(90 - self.cap_deg)

        distance = self.vitesse_km_s * delta_t_s


        self.x += distance * math.cos(cap_rad)
        self.y += distance * math.sin(cap_rad)




