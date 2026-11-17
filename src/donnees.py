import csv
import os


def nettoyage(fichier_csv):
    '''Lecture du fichier CSV et création d'un nouveau 
    fichier CSV avec un nettoyage des données
 '''
    with open(fichier_csv, 'r', encoding="UTF-8") as f1:
        reader = csv.reader(f1)
        with open(os.path.join("donnees", "restaurant_data_nettoye.csv"), "w", newline="", encoding="UTF-8") as f2:
            writer = csv.writer(f2)
            en_tete = next(reader)  # Lire l'en-tête du fichier CSV
            writer.writerow(en_tete[1:3] + en_tete[4:6] + [en_tete[8]]+[en_tete[-1]] )
            for liste in reader:
                writer.writerow(liste[1:3] + liste[4:6] + [liste[8]] + [liste[-1]])