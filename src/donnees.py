import os
import pandas as pd


def nettoyage(fichier_csv):
    """Nettoie le fichier CSV en créant un nouveau fichier avec les colonnes nécessaires seulement."""

    colonnes = [
        "Location", "Cuisine", "Seating Capacity",
        "Average Meal Price", "Chef Experience Years", "Revenue"
    ]

    df = pd.read_csv(fichier_csv)

    colonnes_manquantes = set(colonnes) - set(df.columns)
    #Si le set n'est pas nul, alors on raise une ValueError
    if colonnes_manquantes:
        raise ValueError(f"Colonnes manquantes : {colonnes_manquantes}")

    df[colonnes].to_csv(
        os.path.join("donnees", "restaurant_data_nettoye.csv"),
        index=False
    )

