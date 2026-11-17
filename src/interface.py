import customtkinter as ctk
from exceptions import DonnéeErronéeError, NomDéjaInscritError
import json 

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class RPFApp(ctk.CTk):


    #Initialisation
    def __init__(self):
        """ Initialisation de la classe application avec comme parent la librairie de customTkinter.
        On définit le titre, la taille de la fenêtre, et la grandeur minimum que l'utilisateur peut avoir.
        On définit les couleurs et les méthodes que l'on appelle dès le lancement de l'application ainsi que
        l'historique que l'on souhaite avoir selon le fichier json. À partir du fichier json model, on initialise trois valeurs
        dans 3 attributs. """
        super().__init__()

        # Fenêtre principale
        self.title("RPF - Restaurant Price Finder")
        self.geometry("1100x700")
        self.minsize(900, 600)
        

        # Couleurs
        self.bg_color = "#F4F6F9"
        self.sidebar_color = "#FFFFFF"
        self.primary_color = "#315C8C"
        self.text_color = "#263445"

        self.configure(fg_color=self.bg_color)

        # Configuration des colonnes
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création du menu latéral, de l'historique et de la page d'accueil
        self._historique = self.charger_historique()
        self.create_sidebar()
        self.show_home()

        #Aller chercher les informations du fichier json
        with open("donnees/model.json", "r", encoding="utf-8") as f:
            model = json.load(f)
            self._liste_catégories = model["nom_colonnes"]
            self._liste_location = model["valeurs_location"]
            self._liste_cuisine = model["valeurs_cuisine"]

    # -----------------------------
    # MENU LATERAL
    # -----------------------------

    def create_sidebar(self):
        """Cette méthode sert à créer un menu latéral à gauche de la fenêtre où l'on va pouvoir retrouvé le nom de l'application
        (Label) et son logo (Label), le bouton d'accueil, le bouton de nouvelle analyse et le bouton d'historique des analyses.
        Le menu latéral est sous forme de grille qui change de grandeur selon la grandeur de la fenêtre."""
        self._sidebar = ctk.CTkFrame(
        self,
        width=240,
        corner_radius=0,
        fg_color=self.sidebar_color
        )

        self._sidebar.grid(row=0, column=0, sticky="nsew")
        self._sidebar.grid_propagate(False)

        # Nom de l'application
        self._logo = ctk.CTkLabel(
        self._sidebar,
        text="RPF",
        font=("Arial", 32, "bold"),
        text_color=self.primary_color
        )

        self._logo.pack(pady=(35, 5))

        self._subtitle = ctk.CTkLabel(
        self._sidebar,
        text="Restaurant Price Finder",
        font=("Arial", 11),
        text_color="gray"
        )

        self._subtitle.pack(pady=(0, 40))

        # Boutons du menu
        self._home_button = ctk.CTkButton(
        self._sidebar,
        text="🏠 Home",
        height=45,
        corner_radius=12,
        fg_color="transparent",
        text_color=self.text_color,
        hover_color="#E8EEF5",
        anchor="w",
        font=("Arial", 14),
        command=self.show_home
        )

        self._home_button.pack(
        fill="x", padx=20, pady=8
        )

        self._analysis_button = ctk.CTkButton(
        self._sidebar,
        text="＋ New Analysis",
        height=45,
        corner_radius=12,
        fg_color="transparent",
        text_color=self.text_color,
        hover_color="#E8EEF5",
        anchor="w",
        font=("Arial", 14),
        command=self.show_new_analysis
        )

        self._analysis_button.pack(
        fill="x", padx=20, pady=8
        )

        self._history_button = ctk.CTkButton(
        self._sidebar,
        text="⏰ History of Analysis",
        height=45,
        corner_radius=12,
        fg_color="transparent",
        text_color=self.text_color,
        hover_color="#E8EEF5",
        anchor="w",
        font=("Arial", 14),
        command=self.show_history
        )

        self._history_button.pack(
        fill="x", padx=20, pady=8
        )


# -----------------------------
# ZONE PRINCIPALE
# -----------------------------

    def clear_content(self):
        """Cette méthode sert à effacer le contenu retrouvé dans la page actuel lorsque l'on clique sur un bouton différent du menu latéral
        ou du bouton pour lancer une prédiction ou à la fin du temps d'attente. Ainsi, le contenu se fait effacer et prépare une nouvelle
        "Frame" qui se fera modifié selon la méthode ayant appelé "clear_content" ."""
        if hasattr(self, "content"):
            self._content.destroy()

        
        self._content = ctk.CTkFrame(
        self,
        fg_color=self.bg_color,
        corner_radius=0
        )

        self._content.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=30,
        pady=30
        )

        # -----------------------------
        # PAGE ACCUEIL
        # -----------------------------

    def show_home(self):
        """Cette méthode se produit lorsque le bouton "Home" du menu d'accueil est activé par l'utilisateur. À ce moment, le contenu
        se fait effacé avec la méthode "clear_content" et crée un nouveau contenu contenant différentes informations sur notre application.
        """
        self.clear_content()

        # Titre
        title = ctk.CTkLabel(
        self._content,
        text="Home",
        font=("Arial", 30, "bold"),
        text_color=self.text_color
        )

        title.pack(anchor="w", pady=(10, 25))

        # Section À propos
        about_frame = ctk.CTkFrame(
        self._content,
        fg_color="white",
        corner_radius=15
        )

        about_frame.pack(fill="x", pady=10)

        about_title = ctk.CTkLabel(
        about_frame,
        text="About this website",
        font=("Arial", 19, "bold"),
        text_color=self.primary_color
        )

        about_title.pack(anchor="w", padx=25, pady=(20, 10))

        about_text = ctk.CTkLabel(
        about_frame,
        text=(
        "RPF is an application used to guess the average price of "
        "a meal at a restaurant depending on his features."
        ),
        font=("Arial", 15),
        text_color=self.text_color,
        wraplength=700,
        justify="left"
        )

        about_text.pack(anchor="w", padx=25, pady=(0, 25))

        # Section caractéristiques
        features_frame = ctk.CTkFrame(
        self._content,
        fg_color="white",
        corner_radius=15
        )

        features_frame.pack(fill="x", pady=15)

        features_title = ctk.CTkLabel(
        features_frame,
        text="Features used (5)",
        font=("Arial", 19, "bold"),
        text_color=self.primary_color
        )

        features_title.pack(anchor="w", padx=25, pady=(20, 15))

        features = [
        "• Location (Downtown, Suburban, Rural)",
        "• Type of cuisine (French, American, Italian, Mexican, Indian)",
        "• Seating Capacity",
        "• Average of years the chefs experiences are",
        "• Annual revenue of the restaurant"
        ]

        for feature in features:

            label = ctk.CTkLabel(
            features_frame,
            text=feature,
            font=("Arial", 14),
            text_color=self.text_color
            )

            label.pack(anchor="w", padx=30, pady=5)

        ctk.CTkLabel(
        features_frame,
        text="",
        height=15
        ).pack()
    
    def show_new_analysis(self):
        """Cette méthode est appelé lorsque l'utilisateur clique sur le bouton "Nouvelle analyse". On efface donc l'ancien contenu, mais 
        on n'utilise pas la méthode "clear_content", puisque cette méthode crée un "frame" rédulier, ce qui, fonctionne pour chaque page
        excepté celle-ci où l'on veut un "ScrollableFrame" pour pouvoir dérouler vers les options si la fenêtre est réduite. Cette méthode
        crée 6 questions en "Entry" ou "OptionMenu" pour les données qualitatives. On enregistre chacune des données dans la classe comme
        attributs pour être réutiliser lors de l'appui du lancement de la prédiction. """
        # Conteneur défilable uniquement pour cette page
        
        if hasattr(self, "content"):
            self._content.destroy()

        self._content = ctk.CTkScrollableFrame(
                self,
                fg_color=self.bg_color,
                corner_radius=0
                )

        self._content.grid(
                row=0,
                column=1,
                sticky="nsew",
                padx=30,
                pady=30
                )

        # -----------------------------
        # EN-TÊTE
        # -----------------------------

        header = ctk.CTkFrame(
            self._content,
            fg_color="transparent"
        )
        header.pack(fill="x", pady=(5, 25))

        ctk.CTkLabel(
            header,
            text="New analysis",
            font=("Arial", 30, "bold"),
            text_color=self.text_color
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Please fill out the information to guess the average price of a meal",
            font=("Arial", 13),
            text_color="#8994A3"
        ).pack(anchor="w", pady=(5, 0))

        # -----------------------------
        # CONTENEUR PRINCIPAL
        # -----------------------------

        main_frame = ctk.CTkFrame(
            self._content,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E8ECF1"
        )

        main_frame.pack(fill="x", pady=5)

        # Titre du formulaire
        ctk.CTkLabel(
            main_frame,
            text="Restaurant information",
            font=("Arial", 18, "bold"),
            text_color=self.text_color
        ).pack(anchor="w", padx=30, pady=(25, 5))

        ctk.CTkLabel(
            main_frame,
            text="The 5 features are needed for the prediction.",
            font=("Arial", 12),
            text_color="#8994A3"
        ).pack(anchor="w", padx=30, pady=(0, 20))

        # Nom de l'analyse

        ctk.CTkLabel(
            main_frame,
            text="Analysis name",
            font=("Arial", 13, "bold"),
            text_color="#344054"
        ).pack(anchor="w", padx=30, pady=(5, 7))

        self._nom_analyse = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ex. Italian restaurant - Downtown",
            height=42,
            corner_radius=8,
            fg_color="#F7F8FA",
            border_color="#E5E9EF",
            text_color=self.text_color
        )

        self._nom_analyse.pack(fill="x", padx=30, pady=(0, 15))

        # -----------------------------
        # GRILLE DES CHAMPS
        # -----------------------------

        fields = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )

        fields.pack(fill="x", padx=30)

        fields.grid_columnconfigure((0, 1), weight=1, uniform="col")

        # Style commun des champs
        entry_color = "#F7F8FA"
        border_color = "#E5E9EF"

        def field_label(parent : ctk.CTkFrame, text : str, row : int, column : int):
            """Crée un titre de champ à un emplacement selon une grille où l'on place chacun des 5 caractéristiques."""
            ctk.CTkLabel(
                parent,
                text=text,
                font=("Arial", 13, "bold"),
                text_color="#344054"
            ).grid(
                row=row,
                column=column,
                sticky="w",
                pady=(12, 7),
                padx=(0, 20)
            )

        # 1. Location
        field_label(fields, "Location", 0, 0)

        self._location = ctk.CTkOptionMenu(
            fields,
            values=self._liste_location,
            height=42,
            corner_radius=8,
            fg_color=entry_color,
            button_color="#E9EDF2",
            button_hover_color="#DCE3EB",
            text_color=self.text_color,
            dropdown_fg_color="white",
            dropdown_text_color=self.text_color
        )

        self._location.grid(
            row=1, column=0,
            sticky="ew",
            padx=(0, 20)
        )

        # 2. Seating Capacity
        field_label(fields, "Seating Capacity", 0, 1)

        self._seating_capacity = ctk.CTkEntry(
            fields,
            placeholder_text="Ex. 40",
            height=42,
            corner_radius=8,
            fg_color=entry_color,
            border_color=border_color,
            text_color=self.text_color
        )

        self._seating_capacity.grid(
            row=1, column=1,
            sticky="ew"
        )

        # 3. Expérience
        field_label(fields, "Average of chefs experience in years", 2, 0)

        self._experience = ctk.CTkEntry(
            fields,
            placeholder_text="Ex. 8",
            height=42,
            corner_radius=8,
            fg_color=entry_color,
            border_color=border_color,
            text_color=self.text_color
        )

        self._experience.grid(
            row=3, column=0,
            sticky="ew",
            padx=(0, 20)
        )

        # 4. Cuisine
        field_label(fields, "Type of cuisine", 2, 1)

        self._cuisine = ctk.CTkOptionMenu(
            fields,
            values=self._liste_cuisine,
            height=42,
            corner_radius=8,
            fg_color=entry_color,
            button_color="#E9EDF2",
            button_hover_color="#DCE3EB",
            text_color=self.text_color,
            dropdown_fg_color="white",
            dropdown_text_color=self.text_color
        )

        self._cuisine.grid(
            row=3, column=1,
            sticky="ew"
        )

        # 5. Revenue 
        field_label(fields, "Annual Revenue of the restaurant", 4, 0)

        self._revenue = ctk.CTkEntry(
            fields,
            placeholder_text="Ex. 500000",
            height=42,
            corner_radius=8,
            fg_color=entry_color,
            border_color=border_color,
            text_color=self.text_color
        )

        self._revenue.grid(
            row=5, column=0,
            sticky="ew",
            padx=(0, 20)
        )

        # -----------------------------
        # SÉPARATION
        # -----------------------------

        ctk.CTkFrame(
            main_frame,
            height=1,
            fg_color="#E8ECF1"
        ).pack(fill="x", padx=30, pady=(30, 20))

        # -----------------------------
        # BOUTON DE PRÉDICTION
        # -----------------------------

        bottom = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        ctk.CTkButton(
            bottom,
            text="Start the prediction  →",
            height=44,
            width=220,
            corner_radius=8,
            fg_color=self.primary_color,
            hover_color="#24466D",
            font=("Arial", 14, "bold"),
            command=self.lancer_prediction
        ).pack(side="right")

        # -----------------------------
        # ZONE DE RÉSULTAT
        # -----------------------------

        self._resultat = ctk.CTkLabel(
            self._content,
            text="",
            font=("Arial", 14),
            text_color=self.primary_color,
            justify="left"
        )

        self._resultat.pack(anchor="w", pady=20)

    def lancer_prediction(self):
        """Chaque donnée est récolté et  nous évaluons les réponses avec des try except pour s'assurer que les données 
        sont toutes remplies et valides. Dans le cas contraire, on affiche un message en rouge, puis on retourne rien
        pour terminer la méthode avant que le "loading_screen" soit lancé. Si les valeurs sont correctes, on enregistre
        les données dans un dictionnaire et on lance le "loading_screen"."""
        # Récupération des données
        location = self._location.get()
        seating_capacity = self._seating_capacity.get()
        experience = self._experience.get()
        cuisine = self._cuisine.get()
        revenue = self._revenue.get()
        nom_analyse = self._nom_analyse.get().strip()

        # Vérification des champs
        if not nom_analyse or not seating_capacity or not experience or not revenue:
            self._resultat.configure(
                text="Please fill out every features and the analysis name.",
                text_color="red"
            )
            return

        try:
            seating_capacity = float(seating_capacity)
            experience = float(experience)
            revenue = int(revenue)

            if not 0 < seating_capacity < 1000 or not 0 < experience < 70 or not 0 < revenue:
                raise(DonnéeErronéeError)

            noms_analyse = [d["Name"] for d in self._historique]
            if nom_analyse in noms_analyse:
                raise(NomDéjaInscritError)

        except DonnéeErronéeError:
            self._resultat.configure(
                text="Please enter valid values.",
                text_color="red"
            )
            return
        except NomDéjaInscritError:
            self._resultat.configure(
                text="This name of analysis is already taken. Please choose another.",
                text_color="red"
            )
            return

        # Enregistrement des données
        donnees = {
            "Name": nom_analyse,
            "Location": location,
            "Cuisine": cuisine,
            "Seating Capacity": seating_capacity,
            "Experience": experience,
            "Revenue": revenue
        }


        # Ouverture de la fenêtre de chargement
        self.afficher_loading(donnees)

        
    def afficher_loading(self, donnees : dict):
        """Dans le cas où la méthode "afficher_loading" est appelé, nous effaçons l'ancien contenu de la page et nous ajoutons le contenu
        d'un interface de temps d'attente. Nous avons ajouté une barre de chargement et utiliser une fonction servant à lancer
        une méthode lorsque 2,5 secondes ont été écoulés. Ce temps d'attente n'est pas représentatif du temps réelle à récolter les données
        ,mais sera toujours au-dessus du temps nécessaire pour les récolter. """
        self.clear_content()

        loading_frame = ctk.CTkFrame(
            self._content,
            fg_color="transparent"
        )

        loading_frame.pack(
            expand=True,
            fill="both"
        )

        ctk.CTkLabel(
            loading_frame,
            text="RPF",
            font=("Arial", 35, "bold"),
            text_color=self.primary_color
        ).place(relx=0.5, rely=0.38, anchor="center")

        ctk.CTkLabel(
            loading_frame,
            text="Analysis in progress...",
            font=("Arial", 22, "bold"),
            text_color=self.text_color
        ).place(relx=0.5, rely=0.48, anchor="center")

        ctk.CTkLabel(
            loading_frame,
            text="Analysis of features of the restaurant.",
            font=("Arial", 13),
            text_color="#8994A3"
        ).place(relx=0.5, rely=0.55, anchor="center")

        progress = ctk.CTkProgressBar(
            loading_frame,
            width=280,
            height=8,
            mode="indeterminate",
            progress_color=self.primary_color
        )

        progress.place(relx=0.5, rely=0.63, anchor="center")

        progress.start()
        self._loading_progress = progress

        donnees["Average Meal Price"] = 0

        # Démonstration : 2,5 secondes
        self.after(
            2500,
            lambda: self.afficher_resultats(donnees)
        )

    def afficher_resultats(self, donnees : dict):
        """Une fois le temps de chargement terminé, cette méthode est appelé. Elle efface l'ancien contenu et ajoute les données récoltés
        après le téléchargement incluant le prix estimé selon les caractéristiques. Nous ajoutons le contenu à l'historique et nous
        avons un bouton proposant de revenir à une nouvelle analyse. (Commande pour lancer la méthode "new_analysis")"""
        self.clear_content()

        # Sauvegarde automatique de l'analyse si on ne vient pas de l'historique
        if not donnees in self._historique:
            self.ajouter_historique(donnees)

        # En-tête
        ctk.CTkLabel(
            self._content,
            text=f"Results of the analysis of {donnees["Name"]}",
            font=("Arial", 30, "bold"),
            text_color=self.text_color
        ).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(
            self._content,
            text="Here are the informations on the analysis",
            font=("Arial", 13),
            text_color="#8994A3"
        ).pack(anchor="w", pady=(0, 25))

        # Carte du prix
        price_frame = ctk.CTkFrame(
            self._content,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E8ECF1"
        )

        price_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            price_frame,
            text="AVERAGE MEAL PRICE : ",
            font=("Arial", 12, "bold"),
            text_color="#8994A3"
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            price_frame,
            text=donnees["Average Meal Price"],
            font=("Arial", 30, "bold"),
            text_color=self.primary_color
        ).pack(pady=(5, 25))

        # Carte des caractéristiques
        info_frame = ctk.CTkFrame(
            self._content,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E8ECF1"
        )

        info_frame.pack(fill="x", pady=15)

        ctk.CTkLabel(
            info_frame,
            text="Features analyzed",
            font=("Arial", 18, "bold"),
            text_color=self.text_color
        ).pack(anchor="w", padx=25, pady=(20, 10))

        for nom, valeur in donnees.items():
            if nom == "Name" or nom == "Average Meal Price":
                continue
            ctk.CTkLabel(
                info_frame,
                text=f"{nom} : {valeur}",
                font=("Arial", 14),
                text_color=self.text_color
            ).pack(anchor="w", padx=25, pady=5)

        ctk.CTkButton(
            self._content,
            text="← New analysis",
            width=200,
            height=42,
            corner_radius=8,
            fg_color=self.primary_color,
            hover_color="#24466D",
            command=self.show_new_analysis
        ).pack(anchor="w", pady=15)



    def charger_historique(self):
        """Cette méthode sert à charger l'historique et donc d'avoir accès aux données du fichier json. S'il n'y a pas de fichier, les
        données corresponderont à une liste vide."""
        try:
            with open("donnees/historique.json", "r", encoding="utf-8") as f:
                return json.load(f)

        except FileNotFoundError:
            return []

    def sauvegarder_historique(self):
        """Cette méthode sert à sauvegarder les données dans l'historique du fichier json. L'historique ayant potentiellement eu des données
        d'ajouté, il crée ou recrée un nouveau fichier json avec toutes les informations de l'historique. """
        with open("donnees/historique.json", "w", encoding="utf-8") as f:
            json.dump(self._historique, f, indent=4, ensure_ascii=False)

    def ajouter_historique(self, donnees : dict):
        """Cette méthode ajoute à l'historique (liste de dictionnaire) de nouvelles données, puis les sauvegardent."""
        self._historique.append(donnees)

        self.sauvegarder_historique()

    def show_history(self):
        """Cette méthode se lance lorsque l'utilisater clique sur le bouton pour lancer l'historique des analyses. Elle efface le 
        contenu de la page et ajoute le sien. S'il n'y a pas de données dans l'historique, alors un message est affiché disant que
        nous n'avons pas d'analyses affichés. Sinon, on prend la liste de l'historique (de la plus récente au plus ancien donc
        inversé), puis on crée un bouton pour chaque historique d'une analyse. Si l'on clique sur un historique, on reprend la
        méthode servant à afficher les résultats nous permettant ainsi de revoir les résultats. """
        self.clear_content()

        # Titre
        ctk.CTkLabel(
            self._content,
            text="Analysis History",
            font=("Arial", 30, "bold"),
            text_color=self.text_color
        ).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(
            self._content,
            text="Here you can find all your previous analyses.",
            font=("Arial", 13),
            text_color="#8994A3"
        ).pack(anchor="w", pady=(0, 25))

        # Conteneur des analyses
        history_frame = ctk.CTkScrollableFrame(
            self._content,
            fg_color="white",
            corner_radius=15
        )

        history_frame.pack(fill="both", expand=True)

        if not self._historique:

            ctk.CTkLabel(
                history_frame,
                text="No analysis saved yet.",
                font=("Arial", 15),
                text_color="#8994A3"
            ).pack(pady=40)

            return

        # Création d'un bouton pour chaque analyse
        for analyse in reversed(self._historique):

            bouton = ctk.CTkButton(
                history_frame,
                text=f"📊  {analyse['Name']}     →",
                height=55,
                corner_radius=10,
                fg_color="#F4F6F9",
                hover_color="#E5ECF4",
                text_color=self.text_color,
                font=("Arial", 14, "bold"),
                anchor="w",
                command=lambda a=analyse: self.afficher_resultats(a)
            )

            bouton.pack(
                fill="x",
                padx=15,
                pady=8
            )