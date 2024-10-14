import sys
from cProfile import label

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit

import proc  # Import des procédures


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("mainwindow.ui", self)  # Charger l'interface

        #self.champ_minimal_file_size = self.findChild(QLineEdit, "champ_minimal_file_size")
        self.button_folder_scan.clicked.connect(lambda: proc.choose_directory_to_scan(self))
        self.button_folder_destination.clicked.connect(lambda: proc.choose_directory_to_copie(self))
        self.button_scann.clicked.connect(lambda: proc.copy_files_threaded(self))
        self.button_reset.clicked.connect(lambda: proc.reset_tout(self))
        self.button_annuler.clicked.connect(lambda: proc.stop_or_exit(self))








if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
