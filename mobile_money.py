from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class GestionCash(App):

    def build(self):

        self.solde = 0
        self.monnaie = "USD"
        self.taux = 2500

        self.mot_de_passe_admin = "1234"
        self.admin_connecte = False
        self.historique = []

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        self.label_solde = Label(text=self.afficher_solde(), font_size=20)
        layout.add_widget(self.label_solde)

        boutons = [
            ("Dépôt", self.depot),
            ("Retrait", self.retrait),
            ("Vente Unité", self.vente_unite),
            ("Echange USD/CDF", self.echange),
            ("Changer Taux", self.changer_taux),
            ("Voir Historique", self.voir_historique),
            ("Connexion Admin", self.login_admin),
        ]

        for texte, fonction in boutons:
            btn = Button(text=texte, size_hint=(1, None), height=50)
            btn.bind(on_release=fonction)
            layout.add_widget(btn)

        return layout

    # --------------------
    # AFFICHAGE SOLDE
    # --------------------
    def afficher_solde(self):
        return f"Solde: {self.solde} {self.monnaie}"

    def mettre_a_jour(self):
        self.label_solde.text = self.afficher_solde()

    # --------------------
    # POPUP SIMPLE
    # --------------------
    def popup(self, message):
        box = BoxLayout(orientation="vertical", padding=10)
        box.add_widget(Label(text=message))
        btn = Button(text="Fermer", size_hint=(1, 0.3))
        box.add_widget(btn)
        pop = Popup(title="Message", content=box, size_hint=(0.8, 0.4))
        btn.bind(on_release=pop.dismiss)
        pop.open()

    # --------------------
    # DEPOT
    # --------------------
    def depot(self, instance):

        layout = BoxLayout(orientation="vertical", spacing=10)

        input_montant = TextInput(hint_text="Montant", multiline=False)

        btn = Button(text="Valider")

        layout.add_widget(input_montant)
        layout.add_widget(btn)

        popup = Popup(title="Dépôt", content=layout, size_hint=(0.8, 0.5))

        def valider(x):
            try:
                m = float(input_montant.text)
                self.solde += m
                self.historique.append(f"Dépôt {m} {self.monnaie}")
                self.mettre_a_jour()
                popup.dismiss()
            except:
                self.popup("Montant invalide")

        btn.bind(on_release=valider)
        popup.open()

    # --------------------
    # RETRAIT
    # --------------------
    def retrait(self, instance):

        layout = BoxLayout(orientation="vertical", spacing=10)

        input_montant = TextInput(hint_text="Montant", multiline=False)
        btn = Button(text="Valider")

        layout.add_widget(input_montant)
        layout.add_widget(btn)

        popup = Popup(title="Retrait", content=layout, size_hint=(0.8, 0.5))

        def valider(x):
            try:
                m = float(input_montant.text)
                if m <= self.solde:
                    self.solde -= m
                    self.historique.append(f"Retrait {m} {self.monnaie}")
                    self.mettre_a_jour()
                    popup.dismiss()
                else:
                    self.popup("Solde insuffisant")
            except:
                self.popup("Montant invalide")

        btn.bind(on_release=valider)
        popup.open()

    # --------------------
    # VENTE UNITE
    # --------------------
    def vente_unite(self, instance):

        layout = BoxLayout(orientation="vertical", spacing=10)

        input_montant = TextInput(hint_text="Montant vente", multiline=False)
        btn = Button(text="Valider")

        layout.add_widget(input_montant)
        layout.add_widget(btn)

        popup = Popup(title="Vente Unité", content=layout, size_hint=(0.8, 0.5))

        def valider(x):
            try:
                m = float(input_montant.text)
                self.solde += m
                self.historique.append(f"Vente unité {m}")
                self.mettre_a_jour()
                popup.dismiss()
            except:
                self.popup("Montant invalide")

        btn.bind(on_release=valider)
        popup.open()

    # --------------------
    # ECHANGE USD/CDF
    # --------------------
    def echange(self, instance):

        layout = BoxLayout(orientation="vertical", spacing=10)

        input_montant = TextInput(hint_text="Montant", multiline=False)
        btn_usd = Button(text="USD -> CDF")
        btn_cdf = Button(text="CDF -> USD")

        layout.add_widget(input_montant)
        layout.add_widget(btn_usd)
        layout.add_widget(btn_cdf)

        popup = Popup(title="Echange", content=layout, size_hint=(0.8, 0.6))

        def usd_to_cdf(x):
            try:
                m = float(input_montant.text)
                self.solde = m * self.taux
                self.monnaie = "CDF"
                self.historique.append(f"Echange USD->CDF {m}")
                self.mettre_a_jour()
                popup.dismiss()
            except:
                self.popup("Montant invalide")

        def cdf_to_usd(x):
            try:
                m = float(input_montant.text)
                self.solde = m / self.taux
                self.monnaie = "USD"
                self.historique.append(f"Echange CDF->USD {m}")
                self.mettre_a_jour()
                popup.dismiss()
            except:
                self.popup("Montant invalide")

        btn_usd.bind(on_release=usd_to_cdf)
        btn_cdf.bind(on_release=cdf_to_usd)

        popup.open()

    # --------------------
    # CHANGER TAUX (ADMIN)
    # --------------------
    def changer_taux(self, instance):

        if not self.admin_connecte:
            self.popup("Accès refusé (Admin)")
            return

        layout = BoxLayout(orientation="vertical", spacing=10)
        input_taux = TextInput(hint_text="Nouveau taux", multiline=False)
        btn = Button(text="Valider")

        layout.add_widget(input_taux)
        layout.add_widget(btn)

        popup = Popup(title="Changer Taux", content=layout, size_hint=(0.8, 0.5))

        def valider(x):
            try:
                self.taux = float(input_taux.text)
                self.historique.append(f"Taux changé: {self.taux}")
                popup.dismiss()
            except:
                self.popup("Taux invalide")

        btn.bind(on_release=valider)
        popup.open()

    # --------------------
    # LOGIN ADMIN
    # --------------------
    def login_admin(self, instance):

        layout = BoxLayout(orientation="vertical", spacing=10)
        input_pass = TextInput(hint_text="Mot de passe", password=True, multiline=False)
        btn = Button(text="Connexion")

        layout.add_widget(input_pass)
        layout.add_widget(btn)

        popup = Popup(title="Admin", content=layout, size_hint=(0.8, 0.5))

        def verifier(x):
            if input_pass.text == self.mot_de_passe_admin:
                self.admin_connecte = True
                self.popup("Admin connecté")
                popup.dismiss()
            else:
                self.popup("Mot de passe incorrect")

        btn.bind(on_release=verifier)
        popup.open()

    # --------------------
    # HISTORIQUE
    # --------------------
    def voir_historique(self, instance):

        texte = "\n".join(self.historique[-20:]) if self.historique else "Aucune opération"

        layout = BoxLayout(orientation="vertical", spacing=10)
        layout.add_widget(Label(text=texte))

        btn = Button(text="Fermer", size_hint=(1, 0.3))
        layout.add_widget(btn)

        popup = Popup(title="Historique", content=layout, size_hint=(0.9, 0.7))
        btn.bind(on_release=popup.dismiss)
        popup.open()


GestionCash().run()