import streamlit as st

from functions import load_data

st.title("Partie I : Exploration")

df = load_data()
print(df.head())
st.dataframe(df)