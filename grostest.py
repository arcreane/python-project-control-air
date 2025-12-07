import sys
from EspaceAerien import EspaceAerien
from Radar import Radar
from PySide6.QtWidgets import (
    QApplication, QMessageBox, QFrame, QVBoxLayout, QPushButton, QSlider, QLabel
)
from PySide6.QtCore import Slot, QFile, QIODevice, QTimer
from PySide6.QtUiTools import QUiLoader

RAYON_ESPACE_AERIEN_KM = 4
TEMPS_INTERVALLE_S = 0.1
TIMER_INTERVALLE_MS = int(TEMPS_INTERVALLE_S * 1000)
DELAI_SPAWN_MS = 20000


class AppLogic:
    def __init__(self):
        self.espace_aerien = EspaceAerien(RAYON_ESPACE_AERIEN_KM)
        self.avion_actif = None

        self.compteur_vol = 10

        loader = QUiLoader()
        ui_file_path = "interface0.ui"
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Erreur UI Critique: Impossible d'ouvrir le fichier UI: {ui_file_path}")
            sys.exit(1)

        self.window = loader.load(ui_file)
        ui_file.close()

        self._setup_ui_elements()

        self.timer_simu = QTimer()
        self.timer_simu.timeout.connect(self._update_simulation)
        self.timer_simu.start(TIMER_INTERVALLE_MS)

        self.timer_spawn = QTimer()
        self.timer_spawn.timeout.connect(self.nouvel_avion_timer)
        self.timer_spawn.start(DELAI_SPAWN_MS)

        print(f"Simulation démarrée. Nouvel avion toutes les {DELAI_SPAWN_MS / 1000}s.")

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

        self.lbl_id = self.window.findChild(QLabel, 'label_5')
        self.lbl_alt = self.window.findChild(QLabel, 'label_4')
        self.lbl_vitesse = self.window.findChild(QLabel, 'label_3')
        self.lbl_cap = self.window.findChild(QLabel, 'label')
        self.lbl_fuel = self.window.findChild(QLabel, 'label_2')

    @Slot()
    def _update_simulation(self):
        self.espace_aerien.update_positions(TEMPS_INTERVALLE_S)
        self.radar_widget.update()

        if self.avion_actif:
            if self.avion_actif in self.espace_aerien.liste_avions:
                self.lbl_id.setText(f"Numéro : {self.avion_actif.id_vol}")
                self.lbl_alt.setText(f"Altitude : {self.avion_actif.altitude} m")
                v_aff = int(self.avion_actif.vitesse_km_s * 1000)
                self.lbl_vitesse.setText(f"Vitesse : {v_aff} km/h")
                self.lbl_cap.setText(f"Cap : {self.avion_actif.cap_deg}°")
                self.lbl_fuel.setText(f"Carburant : {self.avion_actif.carburant:.1f}%")
            else:
                self.avion_actif = None
                self._reset_labels()

    @Slot()
    def nouvel_avion_timer(self):
        nom_vol = f"VOL{self.compteur_vol}"
        self.espace_aerien.add_random_avion(nom_vol)
        self.compteur_vol += 1
        self.radar_widget.update()

    def _reset_labels(self):
        self.lbl_id.setText("Numéro : --")
        self.lbl_alt.setText("Altitude : --")
        self.lbl_vitesse.setText("Vitesse : --")
        self.lbl_cap.setText("Cap : --")
        self.lbl_fuel.setText("Carburant : --")

    @Slot(object)
    def on_avion_selected_from_radar(self, avion):
        self.avion_actif = avion
        if avion:
            valeur_slider = int(avion.vitesse_km_s * 1000)
            self.slider_vitesse.blockSignals(True)
            self.slider_vitesse.setValue(valeur_slider)
            self.slider_vitesse.blockSignals(False)
        else:
            self._reset_labels()

    @Slot()
    def vol_monter(self):
        if self.avion_actif: self.avion_actif.monter_palier()

    @Slot()
    def vol_descendre(self):
        if self.avion_actif: self.avion_actif.descendre_palier()

    @Slot()
    def vol_gauche(self):
        if self.avion_actif:
            self.avion_actif.cap_deg = (self.avion_actif.cap_deg - 10) % 360

    @Slot()
    def vol_droite(self):
        if self.avion_actif:
            self.avion_actif.cap_deg = (self.avion_actif.cap_deg + 10) % 360

    @Slot(int)
    def vitesse_changee(self, value):
        if self.avion_actif:
            self.avion_actif.vitesse_km_s = value / 1000.0

    @Slot()
    def atterir(self):
        if self.avion_actif:
            QMessageBox.information(self.window, "Info", f"Atterrissage demandé pour {self.avion_actif.id_vol}")

    def show(self):
        self.window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logic = AppLogic()
    logic.show()
    sys.exit(app.exec())