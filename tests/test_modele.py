import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent/"src"))
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
            "Chef Experience Years": [10.0, 5.0, 3.0, 15.0, 8.0, 2.0, 12.0, 6.0, 4.0, 14.0],
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
            "Average Meal Price": [45.0, 28.0, 18.0, 60.0, 32.0, 16.0, 50.0, 30.0, 20.0, 55.0],
        }
    )

def test_transform_train_vs_inference(df_sample: pd.DataFrame):
    pipeline = MODEL()  # À adapter
    df_train = df_sample.iloc[:6].copy()
    df_val = df_sample.iloc[6:].copy()
    df_val["categorie"] = ["NOUVELLE_CATEGORIE", "A"]

    df_train_enc = pipeline.transform(df_train, is_training=True)
    df_val_enc = pipeline.transform(df_val, is_training=False)

    assert isinstance(df_train_enc, pd.DataFrame)
    assert isinstance(df_val_enc, pd.DataFrame)
    assert list(df_val_enc.columns) == list(df_train_enc.columns)
    assert len(df_val_enc) == len(df_val)


def test_transform_cas_limites_dataframe_vide_et_modalite_unique(df_sample: pd.DataFrame):
    pipeline = MODEL()  # À adapter

    # Cas A : DataFrame vide avec les bonnes colonnes
    df_vide = df_sample.iloc[0:0].copy()
    res_vide = pipeline.transform(df_vide, is_training=True)
    assert len(res_vide) == 0

    # Cas B : une seule modalité unique dans la colonne catégorielle
    df_mono_cat = df_sample.copy()
    df_mono_cat["categorie"] = "UNIQUE"
    res_mono = pipeline.transform(df_mono_cat, is_training=True)
    assert len(res_mono) == len(df_mono_cat)


# ---------------------------------------------------------------------------
# 5 & 6. Tests de train_and_eval(self, df)
# ---------------------------------------------------------------------------


def test_train_and_eval_cas_usuel(df_sample: pd.DataFrame):
    pipeline = MODEL()  # À adapter

    mse, y_val, y_pred = pipeline.train_and_eval(df_sample)

    assert isinstance(mse, (float, np.floating))
    assert mse >= 0.0
    assert len(y_val) == len(y_pred)
    assert len(y_val) > 0

    # Vérification de cohérence de l'EQM avec pytest.approx
    mse_calculee = float(np.mean((np.asarray(y_val) - np.asarray(y_pred)) ** 2))
    assert mse == pytest.approx(mse_calculee, rel=1e-5, abs=1e-5)


def test_train_and_eval_donnees_insuffisantes_ou_cible_constante(df_sample: pd.DataFrame):
    pipeline = MODEL()  # À adapter

    # Cas A : trop peu de lignes pour entraîner/évaluer
    df_trop_petit = df_sample.iloc[:1].copy()
    with pytest.raises(ValueError):
        pipeline.train_and_eval(df_trop_petit)

    # Cas B : présence de NaN non gérés
    df_avec_nan = df_sample.copy()
    df_avec_nan.loc[0, "num_1"] = np.nan
    with pytest.raises(ValueError):
        pipeline.train_and_eval(df_avec_nan)


# ---------------------------------------------------------------------------
# 7 & 8. Tests de save(self, df, model_path, meta_path)
# ---------------------------------------------------------------------------


def test_save_cas_usuel_modele_et_metadonnees(tmp_path: Path, df_sample: pd.DataFrame):
    pipeline = MODEL()  # À adapter
    mse, _, _ = pipeline.train_and_eval(df_sample)

    model_path = tmp_path / "modele.joblib"
    meta_path = tmp_path / "metadonnees.json"

    pipeline.save(df_sample, str(model_path), str(meta_path))

    assert model_path.exists()
    assert meta_path.exists()

    modele_charge = joblib.load(model_path)
    assert modele_charge is not None

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    # À adapter : vérifier les clés exactes de votre dictionnaire de métadonnées
    assert "categorical_values" in meta
    assert "numeric_intervals" in meta
    assert "mse" in meta
    assert meta["mse"] == pytest.approx(mse, rel=1e-5, abs=1e-5)

    # Exemple de vérification d'intervalle numérique (min / max)
    borne_min, borne_max = meta["numeric_intervals"]["num_1"]
    assert borne_min == pytest.approx(df_sample["num_1"].min())
    assert borne_max == pytest.approx(df_sample["num_1"].max())


def test_save_cas_limites_chemin_invalide_et_intervalle_nul(tmp_path: Path, df_sample: pd.DataFrame):
    pipeline = MODEL()  # À adapter
    pipeline.train_and_eval(df_sample)

    # Cas A : dossier parent inexistant pour meta_path
    chemin_invalide = tmp_path / "dossier_absent" / "meta.json"
    with pytest.raises((FileNotFoundError, OSError)):
        pipeline.save(df_sample, str(tmp_path / "modele.joblib"), str(chemin_invalide))

    # Cas B : variable numérique constante (min == max)
    df_const = df_sample.copy()
    df_const["num_1"] = 42.0
    model_path = tmp_path / "modele_const.joblib"
    meta_path = tmp_path / "meta_const.json"

    pipeline.save(df_const, str(model_path), str(meta_path))
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    borne_min, borne_max = meta["numeric_intervals"]["num_1"]
    assert borne_min == pytest.approx(42.0)
    assert borne_max == pytest.approx(42.0)