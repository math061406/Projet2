import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
import joblib
import json


def entrainer(X_train:np.ndarray,y_train:np.ndarray)-> LinearRegression:
    """ Entraîne un modèle de régression linéaire sur les données fournies
        
        Paramètres
        X_train: 
        Matrice des varaiables explicatives pour l'entraînement,
        de forme 
        y_train :
        Vecteurs des valeurs cibles d'entrainement,
        de formes (n_samples)
       """
    modele = LinearRegression()
    modele.fit(X_train,y_train)
    return modele  
def eval(model:LinearRegression,X_val : np.ndarray,y_val:np.ndarray):
    """ Évalue les performances du modèle sur un ensemble de validation
    mse : erreur quadratique moyenne 
    plus le mse est faible, plus le modèle est précis 
    """
    y_pred = model.predict(X_val)
    mse = mean_squared_error(y_val,y_pred)
    return mse 

def main(test_ratio: float = 0.2, random_state: int = 0):
    # transforme le fichier csv en un un tableau structuré appelé dataframe 
    df = pd.read_csv("donnees/restaurant_data_nettoye.csv")
    
    # Transformer les données qualitaves en format numériques pour pouvoir entrainer le modèle
    # Créer différente colonne pour chaque options d'une catégorie et 
    # affiche 1 si l'option est présente à cette ligne et 0 si elle est abscente 
    categorical_columns = df.select_dtypes(include=['str']).columns     #Sélectionne les colonnes avec des données qualitatives 
    encoder = OneHotEncoder(sparse_output=False)
    encoded_data = encoder.fit_transform(df[categorical_columns])
    encoded_df = pd.DataFrame( encoded_data, columns=encoder.get_feature_names_out(categorical_columns))
    final_df = pd.concat([df.drop(columns=categorical_columns), encoded_df],axis=1)


    data_temp = final_df.drop(columns="Average Meal Price")

    # Données utilisées par le modèle pour prédire une valeur 
    X = data_temp  
    # Données que le modèle doit pouvoir prédire                                                      
    y = final_df["Average Meal Price"]


    # Séparer le jeu de données en ensembles d'entraînement et de validation
    # L'ensemble d'entrainement : C'est la portion des données utilisées par le modèle 
    #                             pour apprendre les motifs (patterns) et la relation entre X et y.
    # L'ensemble de validation : C'est le reste des données cachées au modèle pendant que l'entraine

    # mélange les données de manière aléatoire 
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_ratio, random_state=random_state)
    model = entrainer(X_train,y_train)
    mse = eval(model,X_val,y_val)

    filename = 'donnees/model_linear.sav'
    #sauvegarder le modèle 
    joblib.dump(model,open(filename,'wb'))

    # Extraire les paramètre mathématiques pour pouvoir prédire les une valeur plus tard 
    model_data = {
        "coefficients": model.coef_.tolist(),
        "intercept": float(model.intercept_),
        "mse" : mse
    }
    with open("donnees/model_parameters.json", "w") as f:
        json.dump(model_data,f,indent=2)
# Prediction = (input1 x coeff1) + (input2 x coeff2) + (input3 x coeff3) + ... + intercept 
if __name__ == "__main__":
    main()
