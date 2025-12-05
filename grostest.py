import sys
import math
from EspaceAerien import EspaceAerien
from Radar import Radar
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