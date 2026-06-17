import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    import os
    if os.path.exists('data/dataset_clean.csv'):
        return pd.read_csv('data/dataset_clean.csv')

    df = pd.read_csv('data/en.openfoodfacts.org.products.tsv', sep='\t', on_bad_lines='skip', engine='python')
    df = clean(df)
    df.to_csv('data/dataset_clean.csv', index=False)
    return df

def clean(df):
    df = clean_columns(df)
    df = get_best_rows(df)
    print(df)
    return df

def get_best_rows(df, n=25000):
    df_scored = df.copy()
    df_scored["_score"] = df_scored.notna().sum(axis=1)
    df_sorted = df_scored.sort_values("_score", ascending=False).head(n)
    return df_sorted.drop(columns=["_score"])

def get_missing_values(df):
    missing = pd.DataFrame({
        "Colonne": df.columns,
        "Valeurs manquantes": df.isna().sum().values,
        "Pourcentage (%)": (df.isna().sum().values / len(df) * 100).round(2)
    })
    return missing.sort_values("Valeurs manquantes", ascending=False)

def clean_columns(df):
    seuil = 0.65
    df = df.dropna(thresh=len(df) * (1 - seuil), axis=1)

    return remove(df)

def remove(df):
    cols_a_supprimer = [
        # MÃ©tadonnÃ©es techniques
        "code",  # identifiant interne
        "url",  # lien web
        "creator",  # utilisateur qui a crÃ©Ã© l'entrÃ©e
        "created_t",  # timestamp brut
        "created_datetime",  # doublon lisible de created_t
        "last_modified_t",  # timestamp brut
        "last_modified_datetime",  # doublon lisible

        # Tags redondants avec d'autres colonnes
        "brands_tags",  # doublon de brands
        "countries_tags",  # doublon de countries
        "countries_en",  # doublon de countries
        "states_tags",  # doublon de states
        "states_en",  # doublon de states
        "additives_tags",  # doublon de additives
        "additives_en",  # doublon de additives

        # Peu exploitables pour du data mining
        "states",  # statut de complÃ©tion de la fiche
        "ingredients_text",  # texte libre, difficile Ã  exploiter
        "serving_size",  # trÃ¨s peu renseignÃ© et non standardisÃ©
    ]

    df = df.drop(columns=[c for c in cols_a_supprimer if c in df.columns])

    return df