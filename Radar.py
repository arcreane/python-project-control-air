from EspaceAerien import EspaceAerien
from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPixmap
from PySide6.QtCore import Qt, QRect, Signal
import math

RAYON_ESPACE_AERIEN_KM = 4
SIM_WIDTH_KM = 2 * RAYON_ESPACE_AERIEN_KM


class Radar(QFrame):

    avion_selectionne_signal = Signal(object)

    def __init__(self, parent=None, espace_aerien=None):
        super().__init__(parent)
        self.espace_aerien = espace_aerien if espace_aerien is not None else EspaceAerien(RAYON_ESPACE_AERIEN_KM)
        self.setMinimumSize(400, 400)
        self.setMouseTracking(True)

        image_path = "Carte_radar.jpg"
        self.background_pixmap = QPixmap(image_path)

        if self.background_pixmap.isNull():
            print(f"ATTENTION : Impossible de charger l'image : {image_path}")

    def mousePressEvent(self, event):
        """Gère le clic souris pour sélectionner un avion."""
        if event.button() == Qt.LeftButton:
            click_pos = event.position()
            click_x = click_pos.x()
            click_y = click_pos.y()

            rect = self.rect()
            centre_x, centre_y = rect.width() / 2, rect.height() / 2
            echelle_px_par_km = min(rect.width(), rect.height()) / SIM_WIDTH_KM

            avion_trouve = None

            for avion in self.espace_aerien.liste_avions:
                ax_px = avion.x * echelle_px_par_km + centre_x
                ay_px = -avion.y * echelle_px_par_km + centre_y

                dist = math.sqrt((click_x - ax_px) ** 2 + (click_y - ay_px) ** 2)

                if dist < 20:
                    avion_trouve = avion
                    avion.est_selectionne = True
                else:
                    avion.est_selectionne = False

            self.update()
            self.avion_selectionne_signal.emit(avion_trouve)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect: QRect = self.rect()

        if not self.background_pixmap.isNull():
            scaled_bg = self.background_pixmap.scaled(
                rect.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled_bg)
        else:
            painter.fillRect(rect, QColor(0, 0, 0))

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

            cap_rad = math.radians(90 - avion.cap_deg)
            longueur_trait = 20
            x_end = x_px + longueur_trait * math.cos(cap_rad)
            y_end = y_px - longueur_trait * math.sin(cap_rad)

            painter.setPen(QPen(color, 2))
            painter.drawLine(int(x_px), int(y_px), int(x_end), int(y_end))

            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(x_px) - 4, int(y_px) - 4, 8, 8)

            painter.setPen(QPen(QColor(220, 220, 220)))
            texte_etiquette = f"{avion.id_vol}\n{avion.altitude}"
            rect_texte = QRect(int(x_px) + 8, int(y_px) - 20, 100, 40)
            painter.drawText(rect_texte, Qt.AlignLeft, texte_etiquette)

        painter.end()