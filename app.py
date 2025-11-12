import sys


from PySide6 import QtUiTools
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QListView, QFrame
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Slot
from avion import classavion


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()






        # Charger le fichier .ui directement dans cette instance
        self.frame = QFrame(self)
        loader = QtUiTools.QUiLoader()
        loader.registerCustomWidget(MainWindow)

        # Important: charger avec self comme parent pour que les slots soient trouvés
        ui_file_path = "demo.ui"

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
        print("Hello from slot!hhhh")

    @Slot()
    def affichage(self):
        rect = self.frame.geometry()
        self.height = rect.height()
        self.width = rect.width()
        print(self.height,self.width)















def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()