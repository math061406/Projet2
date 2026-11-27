import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent/"src"))
from donnees import nettoyage




def test_nettoyage_cas_usuel():
    """
    Vérifie le fonctionnement de `nettoyage` sur le jeu de données complet.

    Exécute le nettoyage sur `donnees/restaurant_data.csv`, puis contrôle que le
    fichier nettoyé est créé, conserve le nombre de lignes initial et expose les
    colonnes attendues dans le bon ordre.
    """

    csv_entree = "donnees/restaurant_data.csv"

    # Lecture du fichier original
    df_original = pd.read_csv(csv_entree)

    # Exécution du nettoyage
    nettoyage(csv_entree)

    # Lecture du fichier nettoyé
    csv_sortie = "donnees/restaurant_data_nettoye.csv"
    df_nettoye = pd.read_csv(csv_sortie)

    colonnes_attendues = ["Location", "Cuisine", "Seating Capacity", "Average Meal Price", "Chef Experience Years", "Revenue"]

    # Vérifications
    assert Path(csv_sortie).exists()
    assert list(df_nettoye.columns) == colonnes_attendues
    assert len(df_nettoye) == len(df_original)


def test_nettoyage_fichier_inexistant_ou_colonne_manquante():
    """
    Vérifie que `nettoyage` lève les bonnes exceptions sur des entrées invalides.

    Teste deux cas limites : l'absence du fichier CSV d'entrée (attend
    `FileNotFoundError` ou `OSError`) et la suppression d'une colonne requise
    (`Location`, attend `ValueError`).
    """
    # Cas A : fichier inexistant
    with pytest.raises((FileNotFoundError, OSError)):
        nettoyage("donnees/fichier_inexistant.csv")

    # Cas B : colonne requise manquante
    csv_incomplet = "donnees/restaurant_data_incomplet.csv"

    # Lecture du fichier original
    df_original = pd.read_csv("donnees/restaurant_data.csv")

    # Suppression d'une colonne nécessaire
    df_original = df_original.drop(columns=["Location"])

    # Création du fichier incomplet
    df_original.to_csv(csv_incomplet, index=False)

    # Vérification que la ValueError est déclenchée
    with pytest.raises(ValueError):
        nettoyage(csv_incomplet)