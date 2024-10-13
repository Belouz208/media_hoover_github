import os
import logging
from enum import nonmember

from PyQt5.QtWidgets import QFileDialog, QLabel, QLineEdit
import shutil



# Chemin vers le répertoire des logs
log_directory = '/home/belouz/Bureau/Dropbox/PYCHARM/media_hoover/logs'

# Vérifier si le répertoire des logs existe, sinon le créer
if not os.path.exists(log_directory):
    print(f"Création du répertoire de logs : {log_directory}")
    os.makedirs(log_directory)

# Configurer les logs
log_file = os.path.join(log_directory, 'errors.log')
print(f"Fichier de logs : {log_file}")  # Message de débogage
logging.basicConfig(filename=log_file, level=logging.ERROR)


#--------------------------------------------------------------------------------------

def find_files(directory):
    try:
        # Parcourir les fichiers dans le répertoire sélectionné
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.mp4', '.avi', '.jpg', '.png')):
                    print(f"Fichier trouvé: {file}")
                    # Ajoute ici le traitement des fichiers (copie, etc.)
    except Exception as e:
        logging.error(f"Erreur lors de la recherche de fichiers: {e}")


def hide_labels(label_folder_scan, label_folder_destination, parent=None):
    """
    Cache les labels spécifiés.
    """
    label_folder_scan.setVisible(False)
    label_folder_destination.setVisible(False)



def choose_directory_to_scan(parent):
    # Implémentation de la fonction scan_directory
    folder = QFileDialog.getExistingDirectory(parent, "Select Directory")
    if folder:
        # Mettre à jour le label pour afficher le chemin sélectionné
        parent.label_folder_scan.setText(f"{folder}")
        parent.chemin_de_dossier_a_scanner=folder

    else:
        # Mettre à jour le label pour indiquer qu'aucun répertoire n'a été sélectionné
        parent.label_folder_scan.setText("Aucun répertoire sélectionné")
        parent.chemin_de_dossier_a_scanner=None




def choose_directory_to_copie(parent):
    # Implémentation de la fonction scan_directory
    folder = QFileDialog.getExistingDirectory(parent, "Select Directory")
    if folder:
        # Mettre à jour le label pour afficher le chemin sélectionné
        parent.label_folder_destination.setText(f"{folder}")
        parent.chemin_de_dossier_destination = folder
    else:
        # Mettre à jour le label pour indiquer qu'aucun répertoire n'a été sélectionné
        parent.label_folder_destination.setText("Aucun répertoire sélectionné")
        parent.chemin_de_dossier_destination = None


test