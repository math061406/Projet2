import json
import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


class MODEL:
    def __init__(self,model_name: str = None, target_variable: str = "Average Meal Price", test_ratio: float = 0.2, random_state: int = 0):
        self.model_name = model_name
        self.target_variable = target_variable
        self.test_ratio = test_ratio
        self.random_state = random_state
        self.encoder = OneHotEncoder(handle_unknown="ignore",sparse_output=False)

        
        # Si le prix d'un repas n'augmente pas de façon strictement proportionnelle par rapport aux variables numériques, 
        # la régression linéaire se trompe. Le Random Forest s'adapte à ces variations
        self.model = RandomForestRegressor()
        self.model_trivial = DummyRegressor(strategy="mean")
        self.columns_names_raw = []
        self.columns_names = []
        self.metrique = 0 

    def transform(self,df:pd.DataFrame, is_training:bool=True)->pd.DataFrame:
        """
            Transformer les données qualitaves en format numériques pour pouvoir entrainer le modèle.
            
                - Créer différente colonne pour chaque options d'une catégorie et 
                   affiche 1 si l'option est présente à cette ligne et 0 si elle est abscente
            is_training:
                Si vrai on ajuste l'encodeur 
                Sinon, on l'utiliser tel quel et on aligne les colonnes sur celles de l'entrainement
        """
         
        # Sélectionne les colonnes avec des données qualitatives  
        categorical_columns = df.select_dtypes(include=['object','string']).columns
        if is_training:
            # Lors de l'entrainement du modèle, ajuster l'encoder selon les colonnes 

            # Début du code tiré de [1]
            # https://www.geeksforgeeks.org/machine-learning/ml-one-hot-encoding/  
            encoded_data = self.encoder.fit_transform(df[categorical_columns])
            encoded_df = pd.DataFrame(encoded_data, columns=self.encoder.get_feature_names_out(categorical_columns))
            new_df = pd.concat([df.drop(columns=categorical_columns), encoded_df],axis=1)
            # Fin du code tiré de [1]
            self.columns_names = list(new_df)
            return new_df
        else:
            encoded_data = self.encoder.transform(df[categorical_columns])
            encoded_df = pd.DataFrame(encoded_data, columns=self.encoder.get_feature_names_out(categorical_columns))
            new_df = pd.concat([df.drop(columns=categorical_columns), encoded_df],axis=1)
            new_df = new_df[self.columns_names]
            return new_df
    
    def train_and_eval(self,df: pd.DataFrame):
        """ 
            Entraîne un modèle de régression par forêt aléatoire sur les données utilisées    
            Paramètres
            X_train: 
            Matrice des varaiables explicatives pour l'entraînement,
            de forme 
            y_train :
            Vecteurs des valeurs cibles d'entrainement,
            de formes (n_samples)
        """
        """ 
            Évalue les performances du modèle sur un ensemble de validation
            mse : erreur quadratique moyenne 
            plus le mse est faible, plus le modèle est précis 
        """
        X_raw = df.drop(columns =[self.target_variable])
        y = df[self.target_variable]


        # Séparer le jeu de données en ensembles d'entraînement et de validation
        # L'ensemble d'entrainement : C'est la portion des données utilisées par le modèle 
        #                             pour apprendre les motifs (patterns) et la relation entre X et y.
        # L'ensemble de validation : C'est le reste des données cachées au modèle pendant que l'entraine

        # mélange les données de manière aléatoire 
        X = self.transform(X_raw,is_training=True)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=self.test_ratio, random_state=self.random_state)
        
        self.model.fit(X_train,y_train)
        y_pred = self.model.predict(X_val)
        mse = mean_squared_error(y_val,y_pred)

        self.columns_names_raw = list(df.columns)
        self.metrique = mse 
        return self.metrique, y_val, y_pred

    def predict(self,user_input_raw: pd.DataFrame) -> np.ndarray:
        """ Cette fonction prédit une variable selon les données entrées par l'utilisateur"""
        new_columns = self.columns_names_raw[:]
        new_columns.remove(self.target_variable)
        user_input = pd.DataFrame([user_input_raw],columns=new_columns)
        print(user_input)
        X_user = self.transform(user_input,is_training= False)
        print(X_user)
        return self.model.predict(X_user)

    def save(self,df:pd.DataFrame,model_path:str,meta_path:str):
        """
            Cette fonction sauvegarde le modèle et ses 
            données du model dans un fichier JSON.
        """
        #sauvegarder le modèle 
        with open(model_path, 'wb') as f:
            joblib.dump(self.model, f)
        

        model_metadata = {
                'nom_colonnes': self.columns_names_raw,
                'valeurs_location': [variable_possible for variable_possible in df['Location'].unique()],
                'valeurs_cuisine' : [variable_possible for variable_possible in df['Cuisine'].unique()],
                'erreur quadratique moyenne ' : self.metrique
            }
        # Fichier json de métadonnées 
        with open(meta_path,'w',encoding='utf-8') as f:
            json.dump(model_metadata,f,indent=2)
    def trivial_model(self,df: pd.DataFrame):
        X_raw = df.drop(columns =[self.target_variable])
        y = df[self.target_variable]


        X = self.transform(X_raw,is_training=True)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=self.test_ratio, random_state=self.random_state)

        self.model_trivial.fit(X_train,y_train)
        y_pred = self.model_trivial.predict(X_val)
        mse_trivial = mean_squared_error(y_val,y_pred)
 
        return mse_trivial
    def __str__(self):
        return f"Nom du modèle : {self.model_name}, métrique : {self.metrique:.3f}"
class DRAW_MODEL(MODEL):
    def __init__(self,target_variable = "Average Meal Price", test_ratio = 0.2, random_state = 0):
        super().__init__(target_variable, test_ratio, random_state)
    
    def plot_prediction(self,y_val:pd.Series,y_pred:pd.Series):
        """
            Cette fonction créer une digramme qui montre les valeurs 
            réelles en fonction des valeurs prédites et la droite de régression linéaire.
        """
        #Initialise la taille de l'écran 
        plt.figure(figsize=(7,5))                   
        plt.scatter(y_val,y_pred,s=15,alpha=0.4)


        min_val = min(y_val.min(), y_pred.min())
        max_val = max(y_val.max(), y_pred.max())
        plt.plot([min_val, max_val], [min_val, max_val], color="red")

        plt.xlabel("Valeurs réelles")
        plt.ylabel("Valeurs prédites")
        plt.title("Comparaison : Valeurs réelles vs Valeurs prédites")
        plt.savefig("donnees/model_prediction.jpg")
        plt.tight_layout()
        plt.show()


    def plot_correlation_heatmap(self,df:pd.DataFrame):
        """
            Cette fonction montre les lien de corrélation entre 
            les différentes variables du jeu de données 
        """
        plt.figure(figsize=(7, 5))
        new_df = self.transform(df,is_training=True)
        # On ne garde que les colonnes numériques pour calculer la corrélation
        numeric_df = new_df.select_dtypes(include=[np.number])
        
        # Calcul de la matrice de corrélation
        corr = numeric_df.corr()
        
        # Dessin de la heatmap
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Matrice de Corrélation des Variables Numériques")
        plt.savefig("donnees/model_heatmap.jpg")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # 1. Chargement des données
    fichier_csv = os.path.join("donnees", "restaurant_data_nettoye.csv")
    df = pd.read_csv(fichier_csv)

    # 2. Instanciation et entraînement via la classe
    modele = MODEL(model_name = "Restauration", target_variable="Average Meal Price", test_ratio=0.2, random_state=0)
    mse, y_val, y_pred = modele.train_and_eval(df)
    print(f"Modèle entraîné avec succès. MSE : {mse:.3f}")

    # 3. Sauvegarde
    model_path = os.path.join("donnees", "model_RandomForestRegression.sav")
    metadata_path = os.path.join("donnees", "model_metadata.json")
    modele.save(df, model_path, metadata_path)

    # 4. Test de prédiction.
    # user_input = ["Rural","Mexican",100,17,500000]
    # prix_repas = modele.predict(user_input)
    # print(prix_repas)

    # 5. Sauvegarder les diagrammes 
    dessin = DRAW_MODEL()
    dessin.plot_prediction(y_val,y_pred)
    dessin.plot_correlation_heatmap(df)

    # 6. Calculer le MSE avec numpy calcule vectorisé
    y_val = np.array(y_val)
    y_pred = np.array(y_pred)
    mse = np.mean((y_val - y_pred) ** 2)

    print(f"MSE avec numpy : {mse:.3f}")

    # 7. Calcule du MSE à l'aide du modèle trivial
    mse_trivial = modele.trivial_model(df)
    print(f"Modèle entraîné avec succès. MSE Trivial : {mse_trivial:.3f}")
    print(modele)