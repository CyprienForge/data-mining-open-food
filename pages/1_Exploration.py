import pandas as pd
import streamlit as st
from functions import load_data, detect_type

st.title("Partie I : Exploration initiale des données")

st.header("1. Chargement des données")

source = st.radio("Source des données", ["OpenFoodFacts", "Importer un CSV"], index=None)

if source is None:
    st.warning("Veuillez choisir une source de données.")
    st.stop()

match source:
    case "OpenFoodFacts":
        df = load_data()
        st.success("Dataset OpenFoodFacts chargé avec succès.")
    case "Importer un CSV":
        fichier = st.file_uploader("Glissez-déposez ou sélectionnez un fichier CSV", type=["csv"])
        if fichier is not None:
            df = pd.read_csv(fichier)
            st.success(f"Fichier **{fichier.name}** chargé avec succès.")
        else:
            st.warning("Veuillez importer un fichier CSV.")
            st.stop()
    case _:
        st.stop()

st.header("2. Aperçu des données")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Premières lignes")
    st.dataframe(df.head(10))
with col2:
    st.subheader("Dernières lignes")
    st.dataframe(df.tail(10))

st.header("3. Résumé statistique")

c1, c2 = st.columns(2)
c1.metric("Nombre de lignes", df.shape[0])
c2.metric("Nombre de colonnes", df.shape[1])

st.subheader("Description des colonnes")

resume = pd.DataFrame({
    "Colonne": df.columns,
    "Type pandas": df.dtypes.values.astype(str),
    "Type statistique": [detect_type(df[col]) for col in df.columns],
    "Valeurs manquantes": df.isna().sum().values,
    "% manquant": (df.isna().sum().values / len(df) * 100).round(2),
    "Valeurs uniques": df.nunique().values
})

st.dataframe(resume, use_container_width=True)

st.subheader("Statistiques descriptives")
st.dataframe(df.describe().T.round(2), use_container_width=True)