import sys
from EspaceAerien import EspaceAerien
from Radar import Radar
from PySide6.QtWidgets import (
    QApplication, QMessageBox, QFrame, QVBoxLayout, QPushButton, QSlider
)
from PySide6.QtCore import Slot, QFile, QIODevice, QTimer
from PySide6.QtUiTools import QUiLoader

RAYON_ESPACE_AERIEN_KM = 4
TEMPS_INTERVALLE_S = 0.1
TIMER_INTERVALLE_MS = int(TEMPS_INTERVALLE_S * 1000)


class AppLogic:
    def __init__(self):
        self.espace_aerien = EspaceAerien(RAYON_ESPACE_AERIEN_KM)

        self.avion_actif = None

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
        print("Simulation démarrée.")

    def _setup_ui_elements(self):
        radar_placeholder = self.window.findChild(QFrame, 'frame')
        if radar_placeholder:
            self.radar_widget = Radar(parent=radar_placeholder, espace_aerien=self.espace_aerien)
            self.radar_widget.avion_selectionne_signal.connect(self.on_avion_selected_from_radar)

            layout = QVBoxLayout(radar_placeholder)
            layout.addWidget(self.radar_widget)
            radar_placeholder.setLayout(layout)

        btn_atterir = self.window.findChild(QPushButton, 'pushButton_3')
        if btn_atterir: btn_atterir.clicked.connect(self.atterir)

        btn_monter = self.window.findChild(QPushButton, 'pushButton_4')
        if btn_monter: btn_monter.clicked.connect(self.vol_monter)

        btn_descendre = self.window.findChild(QPushButton, 'pushButton_5')
        if btn_descendre: btn_descendre.clicked.connect(self.vol_descendre)

        btn_gauche = self.window.findChild(QPushButton, 'pushButton')
        if btn_gauche: btn_gauche.clicked.connect(self.vol_gauche)

        btn_droite = self.window.findChild(QPushButton, 'pushButton_2')
        if btn_droite: btn_droite.clicked.connect(self.vol_droite)

        self.slider_vitesse = self.window.findChild(QSlider, 'verticalSlider')
        if self.slider_vitesse:
            self.slider_vitesse.setRange(160, 310)
            self.slider_vitesse.valueChanged.connect(self.vitesse_changee)

    @Slot()
    def _update_simulation(self):
        self.espace_aerien.update_positions(TEMPS_INTERVALLE_S)
        self.radar_widget.update()


    @Slot(object)
    def on_avion_selected_from_radar(self, avion):
        """Appelé quand on clique sur le radar."""
        self.avion_actif = avion
        if avion:
            print(f"Sélection : {avion.id_vol}")
            valeur_slider = int(avion.vitesse_km_s * 1000)
            self.slider_vitesse.blockSignals(True)
            self.slider_vitesse.setValue(valeur_slider)
            self.slider_vitesse.blockSignals(False)
        else:
            self.avion_actif = None

    @Slot()
    def vol_monter(self):
        if self.avion_actif:
            if self.avion_actif.monter_palier():
                print(f"{self.avion_actif.id_vol} monte -> {self.avion_actif.altitude}")
                self.radar_widget.update()
        else:
            print("Aucun avion sélectionné.")

    @Slot()
    def vol_descendre(self):
        if self.avion_actif:
            if self.avion_actif.descendre_palier():
                print(f"{self.avion_actif.id_vol} descend -> {self.avion_actif.altitude}")
                self.radar_widget.update()
        else:
            print("Aucun avion sélectionné.")

    @Slot()
    def vol_gauche(self):
        if self.avion_actif:
            self.avion_actif.cap_deg = (self.avion_actif.cap_deg - 10) % 360
            print(f"Virage GAUCHE -> {self.avion_actif.cap_deg}°")
            self.radar_widget.update()
        else:
            print("Aucun avion sélectionné.")

    @Slot()
    def vol_droite(self):
        if self.avion_actif:
            self.avion_actif.cap_deg = (self.avion_actif.cap_deg + 10) % 360
            print(f"Virage DROITE -> {self.avion_actif.cap_deg}°")
            self.radar_widget.update()
        else:
            print("Aucun avion sélectionné.")

    @Slot(int)
    def vitesse_changee(self, value):
        if self.avion_actif:
            nouvelle_vitesse = value / 1000.0
            self.avion_actif.vitesse_km_s = nouvelle_vitesse


    @Slot()
    def atterir(self):
        QMessageBox.information(self.window, "Info", "Atterrissage non implémenté pour l'instant.")

    def show(self):
        self.window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logic = AppLogic()
    logic.show()
    sys.exit(app.exec())