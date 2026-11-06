import csv
import os
#Lecture du fichier CSV et création d'un nouveau fichier CSV avec un nettoyage des données

def nettoyage(fichier_csv):
    with open(fichier_csv, 'r', encoding="UTF-8") as f1:
        reader = csv.reader(f1)
        with open(os.path.join("donnees", "restaurant_data_nettoyé.csv"), "w", newline="", encoding="UTF-8") as f2:
            writer = csv.writer(f2)
            en_tete = next(reader)  # Lire l'en-tête du fichier CSV
            writer.writerow(en_tete[1:6] + [en_tete[8]])
            for liste in reader:
                writer.writerow(liste[1:6] + [liste[8]])
            
