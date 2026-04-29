import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de la page pour mobile
st.set_page_config(page_title="StudioCheck YDE", page_icon="🏠")

st.title("🏠 StudioCheck : Collecte")
st.write("Enregistrez les détails du studio directement sur le terrain.")

# Formulaire de collecte (Critères : Robustesse et Efficacité)
with st.form("form_studio", clear_on_submit=True):
    nom_bailleur = st.text_input("Nom du bailleur / Agence")
    loyer = st.number_input("Loyer mensuel (FCFA)", min_value=0, step=5000)
    quartier = st.text_input("Quartier (ex: Bastos, Ngousso...)")
    etat = st.select_slider("État du studio", options=["Mauvais", "Moyen", "Bon", "Excellent"])
    contact = st.text_input("Contact (Téléphone)")
    
    submit = st.form_submit_button("Enregistrer la visite")

    if submit:
        if nom_bailleur and quartier:
            # Création d'une ligne de données
            nouvelle_donnee = {
                "Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Bailleur": nom_bailleur,
                "Loyer": loyer,
                "Quartier": quartier,
                "Etat": etat,
                "Contact": contact
            }
            # Note : Pour une fiabilité totale, connectez une Google Sheet ici plus tard
            st.success(f"✅ Studio à {quartier} enregistré avec succès !")
            st.balloons()
            st.info("Les données sont prêtes à être exportées ci-dessous.")
        else:
            st.error("Veuillez remplir au moins le nom et le quartier.")

# Affichage des données (Efficacité)
st.divider()
st.subheader("📋 Liste des studios visités")
st.warning("Note : Sur cette version gratuite, les données s'effacent si l'app redémarre. Exportez votre CSV régulièrement !")

# Simulation d'un historique (pour l'exemple)
if 'historique' not in st.session_state:
    st.session_state.historique = []

if submit:
    st.session_state.historique.append(nouvelle_donnee)

if st.session_state.historique:
    df = pd.DataFrame(st.session_state.historique)
    st.dataframe(df)
    st.download_button("📥 Télécharger le rapport CSV", df.to_csv(index=False), "visites_studios.csv")
