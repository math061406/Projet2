import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from modele import MODEL


@pytest.fixture
def df_sample() -> pd.DataFrame:
    """Jeu de données synthétique réutilisable pour les tests."""
    return pd.DataFrame(
        {
            "Location": [
                "Downtown",
                "Suburban",
                "Rural",
                "Downtown",
                "Suburban",
                "Rural",
                "Downtown",
                "Suburban",
                "Rural",
                "Downtown",
            ],
            "Cuisine": [
                "French",
                "Italian",
                "Mexican",
                "American",
                "Indian",
                "French",
                "Italian",
                "Mexican",
                "American",
                "Indian",
            ],
            "Seating Capacity": [50, 80, 40, 120, 60, 30, 90, 70, 45, 110],
            "Chef Experience Years": [
                10.0,
                5.0,
                3.0,
                15.0,
                8.0,
                2.0,
                12.0,
                6.0,
                4.0,
                14.0,
            ],
            "Revenue": [
                800000.0,
                450000.0,
                200000.0,
                1500000.0,
                600000.0,
                150000.0,
                950000.0,
                500000.0,
                250000.0,
                1200000.0,
            ],
            "Average Meal Price": [
                45.0,
                28.0,
                18.0,
                60.0,
                32.0,
                16.0,
                50.0,
                30.0,
                20.0,
                55.0,
            ],
        }
    )


def test_transform_train_vs_inference(df_sample: pd.DataFrame):
    """
    Vérifie que `transform` produit les mêmes colonnes en entraînement et en inférence.

    Ajuste l'encodeur sur `df_train` (`is_training=True`), puis transforme `df_val`
    (`is_training=False`) et contrôle que les deux sorties sont des `DataFrame` avec
    exactement les mêmes colonnes.
    """
    pipeline = MODEL()
    df_train = df_sample.iloc[:6].copy()
    df_val = df_sample.iloc[6:].copy()

    df_val["Cuisine"] = ["French", "Italian", "Indian", "American"]

    df_train_enc = pipeline.transform(df_train, is_training=True)
    df_val_enc = pipeline.transform(df_val, is_training=False)

    assert isinstance(df_train_enc, pd.DataFrame)
    assert isinstance(df_val_enc, pd.DataFrame)
    assert list(df_val_enc.columns) == list(df_train_enc.columns)


def test_transform_cas_limites_dataframe_vide_et_modalite_unique(
    df_sample: pd.DataFrame,
):
    """
    Vérifie le comportement de `transform` lorsqu'une catégorie n'a qu'une modalité.

    Assigne une valeur unique (`"French"`) à `Cuisine` et contrôle que `transform`
    conserve le nombre de lignes du `DataFrame`.
    """
    pipeline = MODEL()

    # une seule modalité unique dans la colonne catégorielle
    df_mono_cat = df_sample.copy()
    df_mono_cat["Cuisine"] = "French"
    res_mono = pipeline.transform(df_mono_cat, is_training=True)
    assert len(res_mono) == len(df_mono_cat)


# ---------------------------------------------------------------------------
# 5 & 6. Tests de train_and_eval(self, df)
# ---------------------------------------------------------------------------


def test_train_and_eval_cas_usuel(df_sample: pd.DataFrame):
    """
    Vérifie l'entraînement et l'évaluation standards de `train_and_eval`.

    Contrôle que la méthode retourne un EQM fini et non négatif, des vecteurs
    `y_val` et `y_pred` de même longueur non nulle, et que l'EQM correspond au
    calcul direct avec `pytest.approx`.
    """
    pipeline = MODEL()  # À adapter

    mse, y_val, y_pred = pipeline.train_and_eval(df_sample)

    assert isinstance(mse, (float, np.floating))
    assert mse >= 0.0
    assert len(y_val) == len(y_pred)
    assert len(y_val) > 0

    # Vérification de cohérence de l'EQM avec pytest.approx
    mse_calculee = float(np.mean((np.asarray(y_val) - np.asarray(y_pred)) ** 2))
    assert mse == pytest.approx(mse_calculee, rel=1e-5, abs=1e-5)


def test_train_and_eval_cible_constante(df_sample: pd.DataFrame):
    """
    Vérifie que `train_and_eval` s'exécute quand la cible `Average Meal Price` est constante.

    Fixe `Average Meal Price` à `50.0` sur toutes les lignes et contrôle que l'EQM
    retourné est numérique et supérieur ou égal à `0.0`.
    """
    pipeline = MODEL()
    df_const_target = df_sample.copy()
    df_const_target["Average Meal Price"] = 50.0

    mse, _, _ = pipeline.train_and_eval(df_const_target)
    assert isinstance(mse, (int, float, np.floating))
    assert mse >= 0.0


# ---------------------------------------------------------------------------
# 7 & 8. Tests de save(self, df, model_path, meta_path)
# ---------------------------------------------------------------------------


def test_save_cas_usuel_modele_et_metadonnees(df_sample: pd.DataFrame):
    """
    Vérifie la sauvegarde du modèle `.joblib` et du fichier de métadonnées JSON.

    Après `train_and_eval`, appelle `save`, recharge le modèle avec `joblib.load`,
    lit le JSON et vérifie la présence de clés attendues ainsi que la cohérence de
    l'EQM enregistrée.
    """
    pipeline = MODEL()  # À adapter
    mse, _, _ = pipeline.train_and_eval(df_sample)

    model_path = "modeles/model_RandomForestRegression.sav"
    meta_path = "modeles/model_metadata.json"


    modele_charge = joblib.load(model_path)
    assert modele_charge is not None

    with open(meta_path) as f:
        meta = json.load(f)
    print(meta)
    # À adapter : vérifier les clés exactes de votre dictionnaire de métadonnées
    dic_keys = list(meta.keys())
    assert dic_keys[0] in meta
    assert dic_keys[2] in meta
    assert dic_keys[3] in meta


def test_save_cas_limites_chemin_invalide_et_intervalle_nul(
    tmp_path: Path, df_sample: pd.DataFrame
):
    """
    Vérifie la gestion d'un dossier parent inexistant et d'une variable constante lors de `save`.

    Contrôle qu'un chemin vers un dossier absent lève `FileNotFoundError` ou `OSError`,
    et prépare un jeu de données avec `Seating Capacity` constante (`39`).
    """
    pipeline = MODEL()  # À adapter
    pipeline.train_and_eval(df_sample)

    # Cas A : dossier parent inexistant pour meta_path
    chemin_invalide = tmp_path / "dossier_absent" / "meta.json"
    with pytest.raises((FileNotFoundError, OSError)):
        pipeline.save(df_sample, str(tmp_path / "modele.joblib"), str(chemin_invalide))

    # Cas B : variable numérique constante (min == max)
    df_const = df_sample.copy()
    df_const["Seating Capacity"] = 39
