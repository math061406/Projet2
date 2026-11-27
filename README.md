Notre projet consiste à prédire le prix moyen d'un repas à un restaurant selon ses caractéristiques. En se fiant à un jeu de données
dans un fichier CSV, nous sommes capable de déterminer à l'aide d'un modèle une valeur estimée du prix moyen que couterait un repas.

Source dataset:
Anthony Therrien. (2024). Restaurant Revenue Prediction Dataset [Dataset]. Kaggle. https://doi.org/10.34740/KAGGLE/DSV/8797164

Commandes d'installation et de lancement:
Pour installer notre programme, il faut télécharger le projet à partir du lien GitHub public.
Une fois installé, on peut exécuter le code qui se retrouve dans "main.py" pour accéder à l'interface.

Structure du code:
Nous avons opté pour la même structure que celle proposé dans l'énoncé du projet 2.



Pages consultés:

CustomTkinter : T. Schimansky, “Documentation Introduction | CustomTkinter,” customtkinter.tomschimansky.com. [En ligne] Disponible: https://customtkinter.tomschimansky.com/documentation/ (Consulté 15 novembre 2026)

Pandas : The pandas development team, "pandas documentation," pandas 3.1.1 documentation. [En ligne] Disponible: https://pandas.pydata.org/docs/ (Consulté 15 novembre)

OneHotEncoder: [1] GeeksforGeeks. (2026) One Hot Encoding in Machine Learning. [En ligne]. Disponible: https://www.geeksforgeeks.org/machine-learning/ml-one-hot-encoding/ (Consulté 14 novembre 2026)


La couverture :
Name Stmts Miss Cover Missing

---

src/donnees.py 11 0 100%
src/exceptions.py 4 0 100%
src/modele.py 118 48 59% 131-142, 144, 147, 155-168, 176-189, 194-227
tests/test_donnees.py 47 0 100%
tests/test_modele.py 55 0 100%

---

TOTAL 235 48 80%


Outil du chapitre 7 utilisé:
Nous avons utilisés deux fois les lambdas dans "interface.py". Les deux lambda servent à pouvoir avoir une référence à une fonction qui possède un paramètre sans lancer la fonction à cause des parenthèses.