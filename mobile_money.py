import json
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

DATA_FILE = "data.json"
ADMIN_PIN = "0000"  # 🔐 Change ici

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "operateurs": {
                "Airtel": {
                    "CDF": {"cash": 500000, "virtuel": 1000000},
                    "USD": {"cash": 1000, "virtuel": 2000}
                }
            },
            "historique": []
        }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

class MainApp(App):

    def build(self):
        self.data = load_data()
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.operateur_spinner = Spinner(
            text="Choisir opérateur",
            values=list(self.data["operateurs"].keys())
        )

        self.devise_spinner = Spinner(
            text="CDF",
            values=["CDF", "USD"]
        )

        self.type_spinner = Spinner(
            text="Type",
            values=["Depot", "Retrait"]
        )

        self.montant_input = TextInput(hint_text="Montant", multiline=False)

        btn_valider = Button(text="Valider Transaction")
        btn_valider.bind(on_press=self.transaction)

        btn_admin = Button(text="Mode Admin")
        btn_admin.bind(on_press=self.admin_login)

        self.message = Label(text="")

        self.layout.add_widget(self.operateur_spinner)
        self.layout.add_widget(self.devise_spinner)
        self.layout.add_widget(self.type_spinner)
        self.layout.add_widget(self.montant_input)
        self.layout.add_widget(btn_valider)
        self.layout.add_widget(btn_admin)
        self.layout.add_widget(self.message)

        return self.layout

    def transaction(self, instance):
        op = self.operateur_spinner.text
        devise = self.devise_spinner.text
        type_op = self.type_spinner.text

        try:
            montant = float(self.montant_input.text)
        except:
            self.message.text = "Montant invalide"
            return

        operateur = self.data["operateurs"][op][devise]

        if type_op == "Retrait" and operateur["cash"] < montant:
            self.message.text = "Solde insuffisant ❌"
            return

        if type_op == "Depot":
            operateur["cash"] += montant
            operateur["virtuel"] -= montant
        else:
            operateur["cash"] -= montant
            operateur["virtuel"] += montant

        self.data["historique"].append({
            "date": str(datetime.now()),
            "operateur": op,
            "type": type_op,
            "montant": montant,
            "devise": devise
        })

        save_data(self.data)
        self.message.text = "Transaction réussie ✅"

    def admin_login(self, instance):
        content = BoxLayout(orientation="vertical")
        pin_input = TextInput(password=True, hint_text="PIN Admin")
        btn = Button(text="Entrer")

        content.add_widget(pin_input)
        content.add_widget(btn)

        popup = Popup(title="Admin Login", content=content, size_hint=(0.8, 0.4))

        def check_pin(instance):
            if pin_input.text == ADMIN_PIN:
                popup.dismiss()
                self.admin_panel()
            else:
                pin_input.text = ""

        btn.bind(on_press=check_pin)
        popup.open()

    def admin_panel(self):
        content = BoxLayout(orientation="vertical")

        new_op_input = TextInput(hint_text="Nom nouvel opérateur")
        btn_add = Button(text="Ajouter")
        btn_delete = Button(text="Supprimer opérateur actuel")

        content.add_widget(new_op_input)
        content.add_widget(btn_add)
        content.add_widget(btn_delete)

        popup = Popup(title="Admin Panel", content=content, size_hint=(0.9, 0.6))

        def add_op(instance):
            nom = new_op_input.text
            if nom:
                self.data["operateurs"][nom] = {
                    "CDF": {"cash": 0, "virtuel": 0},
                    "USD": {"cash": 0, "virtuel": 0}
                }
                save_data(self.data)
                self.operateur_spinner.values = list(self.data["operateurs"].keys())
                new_op_input.text = ""

        def delete_op(instance):
            op = self.operateur_spinner.text
            if op in self.data["operateurs"]:
                del self.data["operateurs"][op]
                save_data(self.data)
                self.operateur_spinner.values = list(self.data["operateurs"].keys())

        btn_add.bind(on_press=add_op)
        btn_delete.bind(on_press=delete_op)

        popup.open()

if __name__ == "__main__":
    MainApp().run()