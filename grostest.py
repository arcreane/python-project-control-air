import sys
import math
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QFrame, QVBoxLayout, QPushButton, QSlider
)
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Slot, QRect, QFile, QIODevice, QTimer
from PySide6.QtUiTools import QUiLoader


RAYON_ESPACE_AERIEN_KM = 7.5
SIM_WIDTH_KM = 2 * RAYON_ESPACE_AERIEN_KM
TEMPS_INTERVALLE_S = 0.1
TIMER_INTERVALLE_MS = int(TEMPS_INTERVALLE_S * 1000)


MIN_SPEED_KM_S = 0.16
MAX_SPEED_KM_S = 0.31




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




class Radar(QFrame):
    def __init__(self, parent=None, espace_aerien=None):
        super().__init__(parent)
        self.espace_aerien = espace_aerien if espace_aerien is not None else EspaceAerien(RAYON_ESPACE_AERIEN_KM)
        self.setMinimumSize(400, 400)
        self.setStyleSheet("background-color: black;")

    def paintEvent(self, event):
        painter = QPainter(self)
        rect: QRect = self.rect()
        centre_x, centre_y = rect.width() / 2, rect.height() / 2
        echelle_px_par_km = min(rect.width(), rect.height()) / SIM_WIDTH_KM


        painter.setPen(QPen(QColor(0, 50, 0), 1))
        painter.drawEllipse(centre_x - RAYON_ESPACE_AERIEN_KM * echelle_px_par_km,
                            centre_y - RAYON_ESPACE_AERIEN_KM * echelle_px_par_km,
                            SIM_WIDTH_KM * echelle_px_par_km,
                            SIM_WIDTH_KM * echelle_px_par_km)


        for avion in self.espace_aerien.liste_avions:
            x_px = avion.x * echelle_px_par_km + centre_x
            y_px = -avion.y * echelle_px_par_km + centre_y

            color = QColor(0, 255, 0)
            if avion.est_en_urgence:
                color = QColor(255, 50, 50)
            elif avion.est_selectionne:
                color = QColor(255, 255, 0)

            painter.setPen(QPen(color, 2))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(x_px - 4, y_px - 4, 8, 8)
            painter.setPen(QPen(QColor(200, 200, 200)))
            painter.drawText(int(x_px) + 5, int(y_px) - 5, avion.id_vol)

        painter.end()


class AppLogic:

    def __init__(self):

        self.espace_aerien = EspaceAerien(RAYON_ESPACE_AERIEN_KM)

        loader = QUiLoader()

        ui_file_path = "interface0.ui"
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Erreur UI Critique: Impossible d'ouvrir le fichier UI: {ui_file_path}")
            sys.exit(1)

        self.window = loader.load(ui_file)
        ui_file.close()

        self._setup_ui_elements()


        self.timer = QTimer()
        self.timer.timeout.connect(self._update_simulation)
        self.timer.start(TIMER_INTERVALLE_MS)
        print(f"Simulation démarrée avec intervalle de {TIMER_INTERVALLE_MS} ms.")

    def _setup_ui_elements(self):
        radar_placeholder = self.window.findChild(QFrame, 'frame')
        if radar_placeholder:
            self.radar_widget = Radar(parent=radar_placeholder, espace_aerien=self.espace_aerien)
            layout = QVBoxLayout(radar_placeholder)
            layout.addWidget(self.radar_widget)
            radar_placeholder.setLayout(layout)
            print("Widget Radar intégré avec succès dans le QFrame 'frame'.")
        else:
            print("ATTENTION: Le widget placeholder 'frame' n'a pas été trouvé dans l'UI.")

        btn_atterir = self.window.findChild(QPushButton, 'pushButton_3')
        if btn_atterir:
            btn_atterir.clicked.connect(self.atterir)

        btn_monter = self.window.findChild(QPushButton, 'pushButton_4')
        if btn_monter:
            btn_monter.clicked.connect(self.vol_monter)

        btn_descendre = self.window.findChild(QPushButton, 'pushButton_5')
        if btn_descendre:
            btn_descendre.clicked.connect(self.vol_descendre)

        btn_gauche = self.window.findChild(QPushButton, 'pushButton')
        if btn_gauche:
            btn_gauche.clicked.connect(self.vol_gauche)

        btn_droite = self.window.findChild(QPushButton, 'pushButton_2')
        if btn_droite:
            btn_droite.clicked.connect(self.vol_droite)

        slider_vitesse = self.window.findChild(QSlider, 'verticalSlider')
        if slider_vitesse:
            slider_vitesse.valueChanged.connect(self.vitesse_changee)

        print("Toutes les connexions ont été tentées manuellement.")

    @Slot()
    def _update_simulation(self):
        """Slot appelé par le QTimer pour mettre à jour la simulation."""


        self.espace_aerien.update_positions(TEMPS_INTERVALLE_S)

        self.radar_widget.update()

    @Slot()
    def atterir(self):
        print("SLOT ATTERIR ACTIVÉ.")
        QMessageBox.information(self.window, "Commande", "Signal d'atterrissage envoyé.")

    @Slot()
    def vol_monter(self):
        QMessageBox.information(self.window, "Commande", "Montée demandée.")

    @Slot()
    def vol_gauche(self):
        QMessageBox.information(self.window, "Commande", "Virage à gauche demandé.")

    @Slot()
    def vol_droite(self):
        QMessageBox.information(self.window, "Commande", "Virage à droite demandé.")

    @Slot()
    def vol_descendre(self):
        QMessageBox.information(self.window, "Commande", "Descente demandée.")

    @Slot(int)
    def vitesse_changee(self, value):
        print(f"Vitesse ajustée à {value}")

    def show(self):
        self.window.show()


# --- Exécution de l'Application ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_app_logic = AppLogic()
    main_app_logic.show()

    sys.exit(app.exec())