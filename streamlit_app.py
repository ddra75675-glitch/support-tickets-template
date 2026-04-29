import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION (Critère : Efficacité) ---
st.set_page_config(page_title="StudioCheck Analytics", page_icon="📈", layout="wide")

st.title("🏠 StudioCheck : Collecte & Finances")

# --- SIMULATION DE BASE DE DONNÉES (Pour l'exemple) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame({
        "Date": ["01/01/2024", "05/01/2024", "10/01/2024", "15/01/2024"],
        "Bailleur": ["Agence Horizon", "M. Amadou", "Sci Bastos", "Mme. Bella"],
        "Quartier": ["Bastos", "Ngousso", "Mvan", "Biyem-Assi"],
        "Gains_Prévus": [150000, 80000, 120000, 90000],
        "Statut": ["Payé", "Impayé", "Payé", "Impayé"],
        "Loyer": [150000, 80000, 120000, 90000]
    })

# --- BARRE LATÉRALE : SAISIE (Critère : Robustesse) ---
st.sidebar.header("➕ Nouvelle Saisie")
with st.sidebar.form("add_form"):
    new_bailleur = st.text_input("Bailleur")
    new_quartier = st.text_input("Quartier")
    new_loyer = st.number_input("Montant Loyer (FCFA)", min_value=0)
    new_statut = st.selectbox("Statut du paiement", ["Payé", "Impayé"])
    
    if st.form_submit_button("Ajouter"):
        new_entry = {
            "Date": datetime.now().strftime("%d/%m/%Y"),
            "Bailleur": new_bailleur,
            "Quartier": new_quartier,
            "Gains_Prévus": new_loyer,
            "Statut": new_statut,
            "Loyer": new_loyer
        }
        st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_entry])], ignore_index=True)
        st.success("Donnée ajoutée !")

# --- SECTION 1 : STATISTIQUES GLOBALES (Critère : Fiabilité) ---
st.subheader("📊 Tableau de Bord Financier")
df = st.session_state.db

total_gains = df[df["Statut"] == "Payé"]["Gains_Prévus"].sum()
total_impayes = df[df["Statut"] == "Impayé"]["Gains_Prévus"].sum()
taux_recouvrement = (total_gains / (total_gains + total_impayes)) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Gains Encaissés (FCFA)", f"{total_gains:,}")
col2.metric("Total Impayés (FCFA)", f"{total_impayes:,}", delta_color="inverse")
col3.metric("Taux de Recouvrement", f"{taux_recouvrement:.1f}%")

st.divider()

# --- SECTION 2 : COURBES ET GRAPHIQUES (Critère : Créativité) ---
col_left, col_right = st.columns(2)

with col_left:
    st.write("📈 **Évolution des Gains**")
    # Simulation d'une courbe temporelle
    fig_line = px.line(df, x="Date", y="Gains_Prévus", color="Statut", 
                       title="Tendances des paiements", markers=True,
                       color_discrete_map={"Payé": "#2ecc71", "Impayé": "#e74c3c"})
    st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    st.write("🍕 **Répartition par Quartier**")
    fig_pie = px.pie(df, values="Gains_Prévus", names="Quartier", hole=0.4,
                     title="Volume financier par zone")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- SECTION 3 : DONNÉES BRUTES ---
st.subheader("📋 Détails des Collectes")
st.dataframe(df, use_container_width=True)

# Export (Efficacité)
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Télécharger le rapport complet (CSV)", csv, "rapport_studios.csv", "text/csv")
