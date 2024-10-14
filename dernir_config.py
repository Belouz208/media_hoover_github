import os
import logging
from PyQt5.QtWidgets import QFileDialog, QApplication
import shutil
from threading import Thread, Event

# Variable globale pour suivre l'état de la copie
copy_in_progress = False
stop_event = Event()  # Événement pour contrôler l'arrêt de la copie

#-------------------------------------------------------------------------------------------

log_directory = '/home/belouz/Bureau/Dropbox/PYCHARM/media_hoover/logs'

if not os.path.exists(log_directory):
    print(f"Création du répertoire de logs : {log_directory}")
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, 'errors.log')
logging.basicConfig(filename=log_file, level=logging.ERROR)

#----------------------------------------------------------------------------------------------------------

def reset_tout(parent):
    parent.label_folder_scan.setText("Aucun répertoire sélectionné")
    parent.label_folder_scan.setStyleSheet("color: red;")
    parent.label_folder_destination.setText("Aucun répertoire sélectionné")
    parent.label_folder_destination.setStyleSheet("color: red;")
    if hasattr(parent, 'champ_minimal_file_size'):
        parent.champ_minimal_file_size.setText("300")

#----------------------------------------------------------------------------------------------------------

def choose_directory_to_scan(parent):
    folder = QFileDialog.getExistingDirectory(parent, "Select Directory")
    if folder:
        parent.label_folder_scan.setText(f"{folder}")
        parent.label_folder_scan.setStyleSheet("color: green;")
        parent.chemin_de_dossier_a_scanner = folder
    else:
        parent.label_folder_scan.setText("Aucun répertoire sélectionné")
        parent.chemin_de_dossier_a_scanner = None

#----------------------------------------------------------------------------------------------------------

def choose_directory_to_copie(parent):
    folder = QFileDialog.getExistingDirectory(parent, "Select Directory")
    if folder:
        parent.label_folder_destination.setText(f"{folder}")
        parent.label_folder_destination.setStyleSheet("color: green;")
        parent.chemin_de_dossier_destination = folder
    else:
        parent.label_folder_destination.setText("Aucun répertoire sélectionné")
        parent.chemin_de_dossier_destination = None

#----------------------------------------------------------------------------------------------------------

def copy_files_threaded(parent):
    global stop_event
    stop_event = Event()  # Réinitialiser l'événement d'arrêt
    thread = Thread(target=copy_files, args=(parent,))
    thread.start()

#----------------------------------------------------------------------------------------------------------

def copy_files(parent):
    global copy_in_progress
    copy_in_progress = True  # Marquer que la copie est en cours

    try:
        if not parent.chemin_de_dossier_a_scanner or not parent.chemin_de_dossier_destination:
            parent.label_folder_scan.setText("Veuillez choisir les dossiers source et destination")
            return

        source_directory = parent.chemin_de_dossier_a_scanner
        destination_directory = parent.chemin_de_dossier_destination

        try:
            min_file_size_kb = int(parent.champ_minimal_file_size.text())
        except ValueError:
            parent.label_msg_err_size.setText("Valeur de taille minimale invalide")
            return

        min_file_size_bytes = min_file_size_kb * 1024

        for root, dirs, files in os.walk(source_directory):
            for file in files:
                if stop_event.is_set():  # Vérifie si l'événement d'arrêt est déclenché
                    print("Copie arrêtée par l'utilisateur.")
                    break
                if file.endswith(('.mp4', '.m4v', '.m4p', '.avi', '.divx', '.mov', '.qt', '.mkv', '.flv', '.wmv', '.webm', '.mpg', '.mpeg', '.mpe', '.mp2', '.3gp', '.3g2', '.f4v', '.f4p', '.f4a', '.f4b', '.ts', '.m2ts', '.mts', '.ogv', '.rm', '.rmvb', '.vob', '.asf')
):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if file_size >= min_file_size_bytes:
                        try:
                            destination_path = os.path.join(destination_directory, file)
                            shutil.copy2(file_path, destination_path)
                            print(f"Fichier copié: {file} ({file_size // 1024} KB)")
                        except Exception as e:
                            logging.error(f"Erreur lors de la copie du fichier {file}: {e}")
                            print(f"Erreur lors de la copie du fichier: {file}")
                    else:
                        print(f"Fichier ignoré (taille insuffisante): {file} ({file_size // 1024} KB)")
            else:
                continue
            break  # Sortir de la boucle principale si l'arrêt est demandé

    except Exception as e:
        logging.error(f"Erreur lors de la copie des fichiers: {e}")
        print(f"Erreur: {e}")

    finally:
        copy_in_progress = False  # La copie est terminée ou annulée

#-------------------------------------------------------------------------------------------------------------

def stop_or_exit(parent):
    global copy_in_progress, stop_event

    if copy_in_progress:
        print("Annulation de la copie en cours...")
        stop_event.set()  # Déclenche l'événement d'arrêt
    else:
        print("Aucune copie en cours, fermeture de l'application...")
        QApplication.quit()  # Fermer le programme principal
