import os
import csv


def nettoyage(fichier_csv):
    '''Lecture du fichier CSV et création d'un nouveau 
    fichier CSV avec un nettoyage des données
 '''
    with open(fichier_csv, 'r', encoding="UTF-8") as f1:
        reader = csv.reader(f1)
        with open(os.path.join("donnees", "restaurant_data_nettoye.csv"), "w", newline="", encoding="UTF-8") as f2:
            writer = csv.writer(f2)
            en_tete = next(reader)  # Lire l'en-tête du fichier CSV
            writer.writerow(en_tete[1:4] + en_tete[5:8])
            for liste in reader:
                writer.writerow(liste[1:4] + liste[5:8])
            
