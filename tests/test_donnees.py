import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent/"src"))
from donnees import nettoyage
from exceptions import DonnéeErronéeError, NomDéjaInscritError

# =====================================================================
# 1. CAS USUELS
# =====================================================================


def test_nettoyage_csv_cas_usuel(tmp_path, monkeypatch):
    """Vérifie l'extraction des colonnes ciblées (1:3, 4:6, 8, -1) dans donnees/restaurant_data_nettoye.csv."""
    monkeypatch.chdir(tmp_path)
    dossier_donnees = tmp_path / "donnees"
    dossier_donnees.mkdir()

    source_csv = dossier_donnees / "raw.csv"
    source_csv.write_text(
        "c0,c1,c2,c3,c4,c5,c6,c7,c8,c9\n"
        "id1,Downtown,French,x,50,10,y,z,800000,45.5\n"
        "id2,Rural,Mexican,x,30,4,y,z,200000,19.0\n",
        encoding="utf-8",
    )

    nettoyage(str(source_csv))

    sortie_csv = dossier_donnees / "restaurant_data_nettoye.csv"
    assert sortie_csv.exists()

    df_nettoye = pd.read_csv(sortie_csv)
    assert list(df_nettoye.columns) == ["c1", "c2", "c4", "c5", "c8", "c9"]
    assert len(df_nettoye) == 2
    assert df_nettoye.loc[0, "c1"] == "Downtown"
    assert df_nettoye.loc[0, "c9"] == pytest.approx(45.5)


# =====================================================================
# 2. CAS LIMITES
# =====================================================================


def test_nettoyage_csv_uniquement_en_tete(tmp_path, monkeypatch):
    """Cas limite : CSV contenant uniquement l'en-tête et aucune ligne de données."""
    monkeypatch.chdir(tmp_path)
    dossier = tmp_path / "donnees"
    dossier.mkdir()

    csv_vide = dossier / "header_only.csv"
    csv_vide.write_text("a,b,c,d,e,f,g,h,i,j\n", encoding="utf-8")

    nettoyage(str(csv_vide))

    df_out = pd.read_csv(dossier / "restaurant_data_nettoye.csv")
    assert len(df_out) == 0
    assert list(df_out.columns) == ["b", "c", "e", "f", "i", "j"]


def test_exceptions_personnalisees_heritent_de_exception():
    """Cas limite : vérifie que les exceptions métier héritent bien d'Exception et portent leur message."""
    with pytest.raises(DonnéeErronéeError, match="hors plage"):
        raise DonnéeErronéeError("Valeur hors plage")

    with pytest.raises(NomDéjaInscritError, match="doublon"):
        raise NomDéjaInscritError("Nom déjà présent (doublon)")


# =====================================================================
# 3. CAS D'ERREUR (pytest.raises)
# =====================================================================


def test_nettoyage_fichier_inexistant_leve_filenotfound():
    """Cas d'erreur : chemin vers un fichier CSV inexistant."""
    with pytest.raises(FileNotFoundError):
        nettoyage("chemin/totalement/inexistant.csv")


def test_nettoyage_ligne_trop_courte_leve_index_error(tmp_path, monkeypatch):
    """Cas d'erreur : ligne ayant moins de 9 colonnes déclenche IndexError sur liste[8]."""
    monkeypatch.chdir(tmp_path)
    dossier = tmp_path / "donnees"
    dossier.mkdir()

    csv_court = dossier / "short.csv"
    csv_court.write_text(
        "c0,c1,c2,c3,c4,c5,c6,c7,c8,c9\n"
        "1,Downtown,French,a,50,10,b,c\n",
        encoding="utf-8",
    )

    with pytest.raises(IndexError):
        nettoyage(str(csv_court))