import pandas as pd
import streamlit as st
from pandas import DataFrame, Series
from pandas.core.interchange.dataframe_protocol import DataFrame
from scipy.stats import skew, kurtosis
from functions import load_data, detect_type, get_data_box
import plotly.express as px

st.set_page_config(
    page_title="Visualisation",
    layout="wide",
)
st.title("Page 3 - Visualisation des données nettoyées")

df = load_data()

col_quant = [col for col in df.columns if detect_type(df[col]) in ["Quantitatif continu", "Quantitatif discret"]]
col_quali = [col for col in df.columns if detect_type(df[col]) in ["Qualitatif nominal", "Qualitatif ordinal"] and col not in ["product_name"]]
cols = col_quant + col_quali

option_col = st.selectbox(
    "Choix des données à visualiser",
    cols,
    index=None, placeholder="Choisir la colonne"
)
option_plt = st.selectbox(
    "Choix de la visualisation",
    ["Histogramme", "Boîte à moustaches", "Matrice de corrélation"],
    index=None, placeholder="Choisir la visualisation"
)

if option_col is None:
    st.warning("Pour visualiser les données du dataset, veuillez sélectionner une colonne !")
    st.stop()

else:
    st.subheader(f"Distribution de {option_col}")

    match option_plt:
        case "Histogramme":
            if option_col in col_quant:
                asymetrie = round(skew(df[option_col].dropna()), 2)
                aplatissement = round(kurtosis(df[option_col].dropna()), 2)

                col1, col2 = st.columns(2)
                col1.metric("Asymétrie", asymetrie)
                col2.metric("Aplatissement", aplatissement)

                fig = px.histogram(df, x=option_col, nbins=30, title=f"Distribution de {option_col}")
            else:
                fig = px.bar(
                    df[option_col].value_counts().reset_index(),
                    x=option_col, y="count",
                    title=f"Distribution de {option_col}"
                )

            st.plotly_chart(fig, use_container_width=True)

        case "Boîte à moustaches":
            if option_col not in col_quant:
                st.warning("La boîte à moustaches n'est disponible que pour les variables quantitatives.")
                st.stop()

            data = df[option_col].dropna()
            Q1, Q3, IQR, borne_min, borne_max, outliers = get_data_box(data)

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Min", f"{data.min():.2f}")
            col2.metric("Q1", f"{Q1:.2f}")
            col3.metric("Médiane", f"{data.median():.2f}")
            col4.metric("Q3", f"{Q3:.2f}")
            col5.metric("Max", f"{data.max():.2f}")

            fig = px.box(
                df,
                y=option_col,
                points="outliers",
                title=f"Boîte à moustaches — {option_col}",
            )

            fig.update_traces(
                marker=dict(
                    color="mediumpurple",
                    size=8,
                    opacity=0.8,
                    symbol="circle-open",
                    line=dict(color="mediumpurple", width=2),
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            if not outliers.empty:
                with st.expander(
                        f"{len(outliers)} valeurs aberrantes — seuils [{borne_min:.2f} ; {borne_max:.2f}]"):
                        st.dataframe(outliers.reset_index(), use_container_width=True
                    )
            else:
                st.success("Aucune valeur aberrante détectée.")

        case "Matrice de corrélation":
            quant_df = df[col_quant].dropna()

            corr = quant_df.corr()

            fig = px.imshow(
                corr,
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                title="Heatmap des corrélations — variables quantitatives",
                aspect="auto",
            )

            fig.update_traces(
                textfont=dict(size=11),
                hovertemplate="%{x} × %{y}<br>r = %{z:.3f}<extra></extra>",
            )

            fig.update_layout(
                coloraxis_colorbar=dict(
                    title="k",
                    tickvals=[-1, -0.5, 0, 0.5, 1],
                    ticktext=["-1", "-0.5", "0", "0.5", "1"],
                ),
                xaxis=dict(tickangle=-45),
            )

            st.plotly_chart(fig, use_container_width=True)

            threshold = st.slider("Seuil k minimum", 0.0, 1.0, 0.7, 0.05)

            strong = corr.unstack().reset_index()
            strong.columns = ["Var A", "Var B", "k"]

            mask = (strong["Var A"] != strong["Var B"]) & (strong["k"].abs() >= threshold)
            strong = (
                strong[mask]
                .drop_duplicates(subset=["k"])
                .sort_values("k", key=abs, ascending=False)
                .reset_index(drop=True)
            )

            if not strong.empty:
                st.dataframe(strong.style.format({"k": "{:.3f}"}), use_container_width=True)
            else:
                st.info(f"Aucune corrélation avec |k| ≥ {threshold}.")

