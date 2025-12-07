import math
import random
from avion import Avion

MIN_SPEED_KM_S = 0.16
MAX_SPEED_KM_S = 0.31


DIST_CRASH_KM = 0.15
DIST_WARNING_KM = 1.5


class EspaceAerien:
    def __init__(self, rayon_km):
        self.liste_avions = []
        self.rayon = rayon_km
        self.pairs_in_danger = set()

        for i in range(3):
            self.add_random_avion(f"START{i + 1}")

    def add_random_avion(self, id_vol):
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

    def update_positions(self, delta_t_s):
        events = {
            "crash": 0,
            "landed": 0,
            "bonus_fuel": 0,
            "avoided": 0
        }

        avions_a_garder = []
        avions_crashes = set()
        ids_atterris = set()

        nb_avions_sortis = 0
        nb_atterrissages_reussis = 0

        for avion in self.liste_avions:
            avion.move(delta_t_s)
            if avion.en_atterrissage and avion.altitude <= 0:
                print(f"Atterrissage REUSSI pour {avion.id_vol}")
                events["landed"] += 1
                ids_atterris.add(avion.id_vol)

                if avion.carburant < 9.0:
                    print(f"!!! BONUS CARBURANT CRITIQUE ({avion.carburant:.1f}%) !!!")
                    events["bonus_fuel"] += 1

                nb_atterrissages_reussis += 1
                continue

            dist_centre = math.sqrt(avion.x ** 2 + avion.y ** 2)
            if dist_centre <= (self.rayon + 0.5):
                avions_a_garder.append(avion)
            else:
                nb_avions_sortis += 1

        current_danger_pairs = set()

        for i in range(len(avions_a_garder)):
            for j in range(i + 1, len(avions_a_garder)):
                av1 = avions_a_garder[i]
                av2 = avions_a_garder[j]

                if av1.altitude == av2.altitude:
                    dist = math.sqrt((av1.x - av2.x) ** 2 + (av1.y - av2.y) ** 2)
                    if dist < DIST_CRASH_KM:
                        print(f"BOOM! Collision entre {av1.id_vol} et {av2.id_vol}")
                        avions_crashes.add(av1)
                        avions_crashes.add(av2)
                        events["crash"] += 1
                    elif dist < DIST_WARNING_KM:
                        pair_id = tuple(sorted((av1.id_vol, av2.id_vol)))
                        current_danger_pairs.add(pair_id)

        for pair in self.pairs_in_danger:
            if pair not in current_danger_pairs:
                id1, id2 = pair
                if id1 not in ids_atterris and id2 not in ids_atterris:
                    crashed_ids = [av.id_vol for av in avions_crashes]
                    if id1 not in crashed_ids and id2 not in crashed_ids:
                        print(f"Sauvetage réussi entre {id1} et {id2}")
                        events["avoided"] += 1

        self.pairs_in_danger = current_danger_pairs

        liste_finale = []
        for avion in avions_a_garder:
            if avion not in avions_crashes:
                liste_finale.append(avion)

        self.liste_avions = liste_finale

        for _ in range(nb_avions_sortis):
            self.add_random_avion(f"RND{random.randint(100, 999)}")

        for _ in range(len(avions_crashes)):
            self.add_random_avion(f"EMG{random.randint(100, 999)}")

        for _ in range(nb_atterrissages_reussis):
            self.add_random_avion(f"NEW{random.randint(1000, 4999)}")
            self.add_random_avion(f"NEW{random.randint(5000, 9999)}")

        return events