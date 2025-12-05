from EspaceAerien import EspaceAerien

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