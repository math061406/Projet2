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
def df_exemple():
    """Jeu de données synthétique suffisant pour train_test_split (test_ratio=0.2)."""
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


# =====================================================================
# 1. CAS USUELS
# =====================================================================


def test_train_and_eval_retourne_mse_coherente(df_exemple):
    """Vérifie l'entraînement et la cohérence numérique de la MSE retournée."""
    modele = MODEL(target_variable="Average Meal Price", test_ratio=0.2, random_state=42)
    mse, y_val, y_pred = modele.train_and_eval(df_exemple)

    mse_attendu = float(np.mean((np.asarray(y_val) - np.asarray(y_pred)) ** 2))
    assert isinstance(mse, float)
    assert mse >= 0.0
    assert mse == pytest.approx(mse_attendu, rel=1e-9)


def test_predict_cas_usuel(df_exemple):
    """Vérifie qu'une prédiction est produite avec la bonne forme et un flottant fini."""
    modele = MODEL(target_variable="Average Meal Price", test_ratio=0.2, random_state=0)
    modele.train_and_eval(df_exemple)

    resultat = modele.predict(["Downtown", "French", 60, 10.0, 850000.0])
    assert resultat.shape == (1,)
    assert float(resultat[0]) == pytest.approx(float(resultat[0]), rel=1e-6)
    assert np.isfinite(resultat[0])


def test_save_genere_modele_et_metadonnees(tmp_path, df_exemple):
    """Vérifie la sauvegarde du modèle (.sav) et du fichier JSON de métadonnées."""
    modele = MODEL(target_variable="Average Meal Price", test_ratio=0.2, random_state=0)
    mse, _, _ = modele.train_and_eval(df_exemple)

    model_path = tmp_path / "model.sav"
    meta_path = tmp_path / "model.json"
    modele.save(df_exemple, str(model_path), str(meta_path))

    assert model_path.exists()
    assert meta_path.exists()

    modele_recharge = joblib.load(model_path)
    assert hasattr(modele_recharge, "predict")

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    assert meta["nom_colonnes"] == list(df_exemple.columns)
    assert set(meta["valeurs_location"]) == {"Downtown", "Suburban", "Rural"}
    assert meta["erreur quadratique moyenne "] == pytest.approx(mse)


# =====================================================================
# 2. CAS LIMITES
# =====================================================================


def test_transform_valeurs_numeriques_flottantes_limites(df_exemple):
    """Cas limite : valeurs numériques très petites ou nulles lors de transform(..., is_training=False)."""
    modele = MODEL(target_variable="Average Meal Price", test_ratio=0.2, random_state=0)
    X_raw = df_exemple.drop(columns=["Average Meal Price"])
    modele.transform(X_raw, is_training=True)

    entree_limite = pd.DataFrame(
        {
            "Location": ["Rural"],
            "Cuisine": ["French"],
            "Seating Capacity": [0],
            "Chef Experience Years": [0.0],
            "Revenue": [0.01],
        }
    )
    X_trans = modele.transform(entree_limite, is_training=False)

    assert len(X_trans) == 1
    assert list(X_trans.columns) == modele.columns_names
    assert X_trans.loc[0, "Seating Capacity"] == pytest.approx(0.0)
    assert X_trans.loc[0, "Revenue"] == pytest.approx(0.01)


# =====================================================================
# 3. CAS D'ERREUR (pytest.raises)
# =====================================================================


def test_predict_categorie_inconnue_leve_value_error(df_exemple):
    """Cas d'erreur : catégorie non vue à l'entraînement provoque une ValueError dans OneHotEncoder."""
    modele = MODEL(target_variable="Average Meal Price", test_ratio=0.2, random_state=0)
    modele.train_and_eval(df_exemple)

    with pytest.raises(ValueError):
        modele.predict(["Mars", "Martian", 50, 5.0, 300000.0])