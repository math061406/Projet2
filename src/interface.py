import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class RPFApp(ctk.CTk):

    def __init__(self):
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

        # Création du menu et de la page
        self.create_sidebar()
        self.show_home()

    # -----------------------------
    # MENU LATERAL
    # -----------------------------

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
        self,
        width=240,
        corner_radius=0,
        fg_color=self.sidebar_color
        )

        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Nom de l'application
        self.logo = ctk.CTkLabel(
        self.sidebar,
        text="RPF",
        font=("Arial", 32, "bold"),
        text_color=self.primary_color
        )

        self.logo.pack(pady=(35, 5))

        self.subtitle = ctk.CTkLabel(
        self.sidebar,
        text="Restaurant Price Finder",
        font=("Arial", 11),
        text_color="gray"
        )

        self.subtitle.pack(pady=(0, 40))

        # Boutons du menu
        self.home_button = ctk.CTkButton(
        self.sidebar,
        text="🏠 Accueil",
        height=45,
        corner_radius=12,
        fg_color=self.primary_color,
        hover_color="#24466D",
        anchor="w",
        font=("Arial", 14),
        command=self.show_home
        )

        self.home_button.pack(
        fill="x", padx=20, pady=8
        )

        self.analysis_button = ctk.CTkButton(
        self.sidebar,
        text="＋ Nouvelle analyse",
        height=45,
        corner_radius=12,
        fg_color="transparent",
        text_color=self.text_color,
        hover_color="#E8EEF5",
        anchor="w",
        font=("Arial", 14),
        command=self.show_new_analysis
        )

        self.analysis_button.pack(
        fill="x", padx=20, pady=8
        )

        self.history_button = ctk.CTkButton(
        self.sidebar,
        text="⏰ Historique analyse",
        height=45,
        corner_radius=12,
        fg_color="transparent",
        text_color=self.text_color,
        hover_color="#E8EEF5",
        anchor="w",
        font=("Arial", 14),
        command=self.show_history
        )

        self.history_button.pack(
        fill="x", padx=20, pady=8
        )

 # -----------------------------
 # ZONE PRINCIPALE
 # -----------------------------

    def clear_content(self):

        if hasattr(self, "content"):
            self.content.destroy()

        self.content = ctk.CTkFrame(
        self,
        fg_color=self.bg_color,
        corner_radius=0
        )

        self.content.grid(
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

        self.clear_content()

        # Titre
        title = ctk.CTkLabel(
        self.content,
        text="Accueil",
        font=("Arial", 30, "bold"),
        text_color=self.text_color
        )

        title.pack(anchor="w", pady=(10, 25))

        # Section À propos
        about_frame = ctk.CTkFrame(
        self.content,
        fg_color="white",
        corner_radius=15
        )

        about_frame.pack(fill="x", pady=10)

        about_title = ctk.CTkLabel(
        about_frame,
        text="À propos",
        font=("Arial", 19, "bold"),
        text_color=self.primary_color
        )

        about_title.pack(anchor="w", padx=25, pady=(20, 10))

        about_text = ctk.CTkLabel(
        about_frame,
        text=(
        "RPF est une application servant à prédire le prix "
        "moyen d'un restaurant selon ses caractéristiques."
        ),
        font=("Arial", 15),
        text_color=self.text_color,
        wraplength=700,
        justify="left"
        )

        about_text.pack(anchor="w", padx=25, pady=(0, 25))

        # Section caractéristiques
        features_frame = ctk.CTkFrame(
        self.content,
        fg_color="white",
        corner_radius=15
        )

        features_frame.pack(fill="x", pady=15)

        features_title = ctk.CTkLabel(
        features_frame,
        text="Caractéristiques utilisées (5)",
        font=("Arial", 19, "bold"),
        text_color=self.primary_color
        )

        features_title.pack(anchor="w", padx=25, pady=(20, 15))

        features = [
        "• Localisation (Ville, Banlieue, Campagne)",
        "• Note attribué au restaurant sur 5",
        "• Nombre d'années d'expérience des chefs",
        "• Type de cuisine (Français, Américain, Italien, Mexicain, Indien)",
        "• Nombre d'abonnées du restaurant sur les réseaux sociaux"
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

        self.clear_content()

        # -----------------------------
        # EN-TÊTE
        # -----------------------------

        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        header.pack(fill="x", pady=(5, 25))

        ctk.CTkLabel(
            header,
            text="Nouvelle analyse",
            font=("Arial", 30, "bold"),
            text_color=self.text_color
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Renseignez les informations du restaurant pour estimer son prix moyen.",
            font=("Arial", 13),
            text_color="#8994A3"
        ).pack(anchor="w", pady=(5, 0))

        # -----------------------------
        # CONTENEUR PRINCIPAL
        # -----------------------------

        main_frame = ctk.CTkFrame(
            self.content,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E8ECF1"
        )

        main_frame.pack(fill="x", pady=5)

        # Titre du formulaire
        ctk.CTkLabel(
            main_frame,
            text="Informations du restaurant",
            font=("Arial", 18, "bold"),
            text_color=self.text_color
        ).pack(anchor="w", padx=30, pady=(25, 5))

        ctk.CTkLabel(
            main_frame,
            text="Les cinq caractéristiques nécessaires à la prédiction.",
            font=("Arial", 12),
            text_color="#8994A3"
        ).pack(anchor="w", padx=30, pady=(0, 20))

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

        # Fonction pour créer un titre de champ
        def field_label(parent, text, row, column):

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

        # 1. Localisation
        field_label(fields, "Localisation", 0, 0)

        self.localisation = ctk.CTkOptionMenu(
            fields,
            values=["Ville", "Banlieue", "Campagne"],
            height=42,
            corner_radius=8,
            fg_color=entry_color,
            button_color="#E9EDF2",
            button_hover_color="#DCE3EB",
            text_color=self.text_color,
            dropdown_fg_color="white",
            dropdown_text_color=self.text_color
        )

        self.localisation.grid(
            row=1, column=0,
            sticky="ew",
            padx=(0, 20)
        )

        # 2. Note
        field_label(fields, "Note du restaurant (sur 5)", 0, 1)

        self.note = ctk.CTkEntry(
            fields,
            placeholder_text="Ex. 4.5",
            height=42,
            corner_radius=8,
            fg_color=entry_color,
            border_color=border_color,
            text_color=self.text_color
        )

        self.note.grid(
            row=1, column=1,
            sticky="ew"
        )

        # 3. Expérience
        field_label(fields, "Expérience des chefs (années)", 2, 0)

        self.experience = ctk.CTkEntry(
            fields,
            placeholder_text="Ex. 8",
            height=42,
            corner_radius=8,
            fg_color=entry_color,
            border_color=border_color,
            text_color=self.text_color
        )

        self.experience.grid(
            row=3, column=0,
            sticky="ew",
            padx=(0, 20)
        )

        # 4. Cuisine
        field_label(fields, "Type de cuisine", 2, 1)

        self.cuisine = ctk.CTkOptionMenu(
            fields,
            values=[
                "Français",
                "Américain",
                "Italien",
                "Mexicain",
                "Indien"
            ],
            height=42,
            corner_radius=8,
            fg_color=entry_color,
            button_color="#E9EDF2",
            button_hover_color="#DCE3EB",
            text_color=self.text_color,
            dropdown_fg_color="white",
            dropdown_text_color=self.text_color
        )

        self.cuisine.grid(
            row=3, column=1,
            sticky="ew"
        )

        # 5. Abonnés
        field_label(fields, "Nombre d'abonnés", 4, 0)

        self.abonnes = ctk.CTkEntry(
            fields,
            placeholder_text="Ex. 25000",
            height=42,
            corner_radius=8,
            fg_color=entry_color,
            border_color=border_color,
            text_color=self.text_color
        )

        self.abonnes.grid(
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
            text="Lancer la prédiction  →",
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

        self.resultat = ctk.CTkLabel(
            self.content,
            text="",
            font=("Arial", 14),
            text_color=self.primary_color,
            justify="left"
        )

        self.resultat.pack(anchor="w", pady=20)

    def lancer_prediction(self):

        # Récupération des données
        localisation = self.localisation.get()
        note = self.note.get()
        experience = self.experience.get()
        cuisine = self.cuisine.get()
        abonnes = self.abonnes.get()

        # Vérification des champs
        if not note or not experience or not abonnes:
            self.resultat.configure(
                text="Veuillez remplir tous les champs.",
                text_color="red"
            )
            return

        try:
            note = float(note)
            experience = float(experience)
            abonnes = int(abonnes)

            if not 0 <= note <= 5 or experience < 0 or abonnes < 0:
                raise ValueError

        except ValueError:
            self.resultat.configure(
                text="Veuillez entrer des valeurs valides.",
                text_color="red"
            )
            return

        # Affichage temporaire des données
        self.resultat.configure(
            text=(
                f"Analyse prête !\n"
                f"Localisation : {localisation}\n"
                f"Note : {note}/5\n"
                f"Expérience : {experience} ans\n"
                f"Cuisine : {cuisine}\n"
                f"Abonnés : {abonnes}"
            ),
            text_color=self.primary_color
        )

        # Résultat
        self.resultat = ctk.CTkLabel(
            self.content,
            text="",
            font=("Arial", 16, "bold"),
            text_color=self.primary_color
        )
        self.resultat.pack(anchor="w", pady=15)



    def show_history(self):

        self.clear_content()

        ctk.CTkLabel(
        self.content,
        text="Historique analyse",
        font=("Arial", 30, "bold"),
        text_color=self.text_color
        ).pack(anchor="w", pady=20)

        ctk.CTkLabel(
        self.content,
        text="Les anciennes analyses seront affichées ici.",
        font=("Arial", 16)
        ).pack(anchor="w", pady=10)


if __name__ == "__main__":

    app = RPFApp()
    app.mainloop()