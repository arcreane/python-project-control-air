import sys


from PySide6 import QtUiTools
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QListView, QFrame
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Slot
from matplotlib.backend_bases import button_press_handler, MouseEvent
import random as rnd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Charger le fichier .ui directement dans cette instance
        self.frame = QFrame(self)
        loader = QtUiTools.QUiLoader()
        loader.registerCustomWidget(MainWindow)

        # Important: charger avec self comme parent pour que les slots soient trouvés
        ui_file_path = "interface0.ui"

        # Méthode alternative: utiliser loadUi (si disponible)
        from PySide6.QtUiTools import loadUiType

        try:
            # Charger et appliquer l'UI directement sur self
            ui_class, _ = loadUiType(ui_file_path)
            self.ui = ui_class()
            self.ui.setupUi(self)
        except:
            # Fallback: méthode manuelle
            from PySide6.QtCore import QFile, QIODevice
            ui_file = QFile(ui_file_path)
            if not ui_file.open(QIODevice.ReadOnly):
                print(f"Erreur: Impossible d'ouvrir le fichier UI")
                sys.exit(-1)

            # Charger avec self comme parent
            loader.load(ui_file, self)
            ui_file.close()

    @Slot()
    def demo(self):
        """Slot appelé lorsque le bouton est cliqué"""
        QMessageBox.information(self, "Message", "Hello! Le bouton a été cliqué!")
        print("Hello from slot!")


class Radar(QFrame):
    def __init__(self, parent = None, espace_aerien = None):
        super().__init__(parent)
        self.espace_aerien = espace_aerien
        self.setMouseTracking(True)
        self.setMinimumSize(400, 400)
    def paintEvent(self, event):
        for avion in self.espace_aerien:
            painter = QPainter(self)
            rect = self.rect()
            painter.fillRect(rect, QColor(255, 255, 255))
            try:

                SIM_WIDTH_KM = 2 * RAYON_ESPACE_AERIEN_KM
            except NameError:
                SIM_WIDTH_KM = 100

            echelle_px_par_km = min(rect.width(), rect.height()) / SIM_WIDTH_KM
            centre_x, centre_y = rect.width() / 2, rect.height() / 2


            for avion in self.espace_aerien.liste_avions:


                x_px = avion.x * echelle_px_par_km + centre_x
                y_px = -avion.y * echelle_px_par_km + centre_y


                color = QColor(0, 255, 0)
                if avion.est_en_urgence:
                    color = QColor(255, 0, 0)
                elif avion.est_selectionne:
                    color = QColor(255, 255, 0)

                painter.setPen(QPen(color, 2))
                painter.setBrush(QBrush(color))


                painter.drawEllipse(x_px - 4, y_px - 4, 8, 8)


                painter.setPen(QPen(QColor(255, 255, 255)))
                painter.drawText(x_px + 5, y_px + 5, avion.id_vol)

            painter.end()


class EspaceAerien:
    def __init__(self, rayon_km):
        self.list_avion = []

    def avionenplus(self,avion):
        self.list_avion.append(avion)
"""
    def collision(self):
        for i in self.list_avion:
"""

















def main():
    app = QApplication(sys.argv)

    ui_file = QFile("interface0.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()