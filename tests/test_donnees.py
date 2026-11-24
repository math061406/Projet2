import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent/"src"))
from donnees import nettoyage

# ---------------------------------------------------------------------------
# 1 & 2. Tests de nettoyage(fichier_csv)
# ---------------------------------------------------------------------------


def test_nettoyage_cas_usuel(tmp_path: Path, df_sample: pd.DataFrame):
    csv_entree = "donnees/restaurant_data.csv"
    df_sample.to_csv(csv_entree, index=False)

    # À adapter : récupérer le chemin retourné ou la convention de nommage du fichier créé
    nettoyage(csv_entree)
    csv_sortie = "donnees/restaurant_data_nettoyage.csv"
    df_nettoye = pd.read_csv(csv_sortie)

    # À adapter : liste exacte des colonnes attendues après sélection
    colonnes_attendues = ["Location", "Cuisine", "Seating Capacity", "Average Meal Price", "Chef Experience Years", "Revenue"]
    assert Path(csv_sortie).exists()
    assert list(df_nettoye.columns) == colonnes_attendues
    assert len(df_nettoye) == len(df_sample)


def test_nettoyage_fichier_inexistant_ou_colonne_manquante(tmp_path: Path, df_sample: pd.DataFrame):
    # Cas A : fichier inexistant
    with pytest.raises((FileNotFoundError, OSError)):
        nettoyage(str(tmp_path / "introuvable.csv"))

    # Cas B : colonne requise manquante
    csv_incomplet = tmp_path / "incomplet.csv"
    df_sample.drop(columns=["num_1"]).to_csv(csv_incomplet, index=False)

    with pytest.raises((KeyError, ValueError)):
        nettoyage(str(csv_incomplet))