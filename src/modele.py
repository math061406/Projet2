import joblib
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder





class MODEL:
    def __init__(self,name_model: str = None,target_variable: str = "Average Meal Price", test_ratio: float = 0.2, random_state: int = 0):
        self.name_model = name_model
        self.target_variable = target_variable
        self.test_ratio = test_ratio
        self.random_state = random_state

        self.model = LinearRegression()
        self.metrique = 0 

    def transform(self,df:pd.DataFrame, is_training:True)->pd.DataFrame:
        """
            Transformer les données qualitaves en format numériques pour pouvoir entrainer le modèle
            Créer différente colonne pour chaque options d'une catégorie et 
            affiche 1 si l'option est présente à cette ligne et 0 si elle est abscente
        """
         
        encoder = OneHotEncoder(sparse_output=False)
        if is_training:
            # Sélectionne les colonnes avec des données qualitatives  
            categorical_columns = df.select_dtypes(include=['string','object']).columns 
            encoded_data = encoder.fit_transform(df[categorical_columns])
        else:
            encoded_data = encoder.transform(df[categorical_columns])

        encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))
        new_df = pd.concat([df.drop(columns=categorical_columns), encoded_df],axis=1)

        return new_df
    
    def train_and_eval(self,df: pd.DataFrame):
        """ 
        Entraîne un modèle de régression linéaire sur les données fournies    
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
        self.metrique = mse 
        return self.metrique, y_val, y_pred

    def predict(self,user_input: pd.DataFrame) -> np.ndarray:
        """ Cette fonction prédit une variable selon les données entrées par l'utilisateur"""
        X_user = self.transform(user_input,is_training= False)
        return self.model.predict(X_user)

    def save(self,df:pd.DataFrame,model_path:str,meta_path:str):
        """
            Cette fonction sauvegarde le modèle et ses 
            données du model dans un fichier JSON.
        """
        #sauvegarder le modèle 
        joblib.dump(self.model,open(model_path,'wb'))

        model_metadata = {
                'nom_colonnes': [titre for titre in df.columns],
                'valeurs_location': [variable_possible for variable_possible in df['Location'].unique()],
                'valeurs_cuisine' : [variable_possible for variable_possible in df['Cuisine'].unique()],
                'erreur quadratique moyenne ' : self.metrique
            }
        # Fichier json de métadonnées 
        with open(meta_path,'w',encoding='utf-8') as f:
            json.dump(model_metadata,f,indent=2)

class DRAW_MODEL(MODEL):
    def __init__(self, name_model = None, target_variable = "Average Meal Price", test_ratio = 0.2, random_state = 0):
        super().__init__(name_model, target_variable, test_ratio, random_state)
    
    def plot_prediction(self,y_val,y_pred):
        """
        Cette fonction créer une digramme qui montre les valeurs 
        réelles en fonction des valeurs prédites et la droite de régression linéaire.
        """

        plt.figure(figsize=(7,5))                   #Initialise la taille de l'écran 
        plt.scatter(y_val,y_pred,s=15,alpha=0.4)
        x_line = np.linspace(y_val.min(),y_val.max(),12).reshape(1,-1)
        y_line = self.model.predict(x_line)
        plt.plot(x_line,y_line, color= "red",label="Droite de régression")
        plt.xlabel("Valeurs réelles")
        plt.ylabel("Valeurs prédites")
        plt.title("Comparaison : Valeurs réelles vs Valeurs prédites")
        plt.show()

    def plot_correlation_heatmap(self,df:pd.DataFrame):
        """
        Cette fonction montre les lien de corrélation entre 
        les différentes variables du jeu de données 
        """
        plt.figure(figsize=(8, 6))
        
        # On ne garde que les colonnes numériques pour calculer la corrélation
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Calcul de la matrice de corrélation
        corr = numeric_df.corr()
        
        # Dessin de la heatmap
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Matrice de Corrélation des Variables Numériques")
        plt.show()


if __name__ == "__main__":
    # 1. Chargement des données
    df = pd.read_csv("donnees/restaurant_data_nettoye.csv")

    # 2. Instanciation et entraînement via la classe
    createur_modele = MODEL(target_variable="Average Meal Price", test_ratio=0.2, random_state=0)
    mse, X_val, y_val = createur_modele.train_and_eval(df)
    print(f"Modèle entraîné avec succès. MSE : {mse:.2f}")

    # 3. Sauvegarde
    createur_modele.save(df, 'donnees/model_linear.sav', 'donnees/model.json')

    