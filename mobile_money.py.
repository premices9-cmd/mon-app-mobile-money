import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Gestion Mobile Money", layout="centered")

# --- SYSTÈME DE SÉCURITÉ SIMPLE ---
def check_password():
    """Retourne True si l'utilisateur a saisi le bon mot de passe."""
    def password_entered():
        if st.session_state["password"] == "1234": # 🚩 CHANGEZ VOTRE CODE ICI
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Ne pas garder le mot de passe en mémoire
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Affichage de l'écran de connexion
        st.title("🔐 Accès Sécurisé")
        st.text_input("Entrez votre code PIN :", type="password", on_change=password_entered, key="password")
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("❌ Code incorrect. Veuillez réessayer.")
        return False
    return True

# Si le mot de passe est correct, on affiche l'application
if check_password():

    # --- INITIALISATION DES DONNÉES ---
    if 'solde_cash' not in st.session_state:
        st.session_state.solde_cash = 500000 
    if 'solde_virtuel' not in st.session_state:
        st.session_state.solde_virtuel = 1000000
    if 'historique' not in st.session_state:
        st.session_state.historique = pd.DataFrame(columns=["Heure", "Type", "Montant", "Client", "Commission"])

    # --- INTERFACE PRINCIPALE ---
    st.title("📲 Ma Caisse Mobile Money")
    
    # Affichage des soldes avec un design épuré
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Cash en Caisse", f"{st.session_state.solde_cash:,} FC")
    with col2:
        st.metric("📱 Solde Virtuel", f"{st.session_state.solde_virtuel:,} FC")

    st.markdown("---")

    # --- FORMULAIRE D'OPÉRATION ---
    st.subheader("Nouvelle Transaction")
    with st.form("transaction_form", clear_on_submit=True):
        type_op = st.selectbox("Type d'opération", ["Dépôt Client", "Retrait Client", "Vente Crédit"])
        montant = st.number_input("Montant (FC)", min_value=0, step=500)
        num_client = st.text_input("Numéro du client (Optionnel)")
        
        # Calcul automatique de commission (Exemple simplifié basé sur votre Excel)
        # On pourrait affiner selon vos grilles exactes
        comm_estimee = montant * 0.01 if type_op == "Retrait Client" else 0
        
        submit = st.form_submit_button("✅ Enregistrer et Valider")

        if submit:
            heure_actuelle = datetime.now().strftime("%H:%M")
            
            if type_op == "Dépôt Client":
                st.session_state.solde_cash += montant
                st.session_state.solde_virtuel -= montant
            elif type_op == "Retrait Client":
                st.session_state.solde_cash -= montant
                st.session_state.solde_virtuel += montant
            
            # Mise à jour de l'historique
            nouvelle_ligne = {
                "Heure": heure_actuelle, 
                "Type": type_op, 
                "Montant": montant, 
                "Client": num_client, 
                "Commission": comm_estimee
            }
            st.session_state.historique = pd.concat([pd.DataFrame([nouvelle_ligne]), st.session_state.historique], ignore_index=True)
            st.success(f"Opération réussie ! Nouveau solde cash : {st.session_state.solde_cash:,} FC")

    # --- TABLEAU DES OPÉRATIONS ---
    st.subheader("📜 Journal du jour")
    st.dataframe(st.session_state.historique, use_container_width=True)

    # Bouton de déconnexion
    if st.sidebar.button("Se déconnecter"):
        st.session_state["password_correct"] = False
        st.rerun()
