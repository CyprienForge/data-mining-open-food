import streamlit as st

st.set_page_config(
    page_title="FIFA 21 - Datamining",
    layout="wide",
)

st.title("Datamining - Statistiques des joueurs FIFA 21")

st.markdown("""
    Ce projet analyse un dataset complet des statistiques des joueurs du jeu **FIFA 21**. 
    L'objectif est d'appliquer des techniques de datamining pour
    explorer, nettoyer, visualiser et modéliser les données afin d'en extraire des
    informations pertinentes sur les profils et performances des joueurs.
""")

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Contenu du dataset")
    st.markdown("""
        - Plus de **18 000 joueurs** recensés dans le jeu
        - Plus de **100 attributs** par joueur : techniques, physiques, mentaux
        - Informations générales : club, nationalité, poste, valeur marchande, salaire
        - Statistiques de performance : vitesse, tir, passe, dribble, défense, physique
        - Données sur les contrats, le potentiel et l'âge
    """)

with col2:
    st.subheader("Etapes du projet")
    st.markdown("""
        1. **Exploration** — apercu general du dataset, types de variables, valeurs manquantes
        2. **Nettoyage** — suppression des colonnes redondantes, gestion des valeurs aberrantes
        3. **Visualisation** — distributions, correlations, comparaisons entre postes et clubs
        4. **Reduction de dimension** — ACP pour synthétiser les attributs de performance
        5. **Clustering** — regroupement des joueurs par profil similaire
    """)

st.divider()

st.subheader("Pipeline du projet")
st.image("pipeline.png", use_container_width=True)