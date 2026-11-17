from donnees import nettoyage
import os
import interface

fichier_csv = os.path.join("donnees", "restaurant_data.csv")
nettoyage(fichier_csv)

if __name__ == "__main__":

    app = interface.RPFApp()
    app.mainloop()