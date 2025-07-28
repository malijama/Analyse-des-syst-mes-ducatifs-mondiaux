import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données
@st.cache_data
def load_data():
    data = pd.read_csv("datasets_projet_2/EdStatsData.csv")
    countries = pd.read_csv("datasets_projet_2/EdStatsCountry.csv")
    return data, countries

data, countries = load_data()

# Nettoyage et fusion
df = data.merge(countries[['Country Code', 'Region', 'Income Group']], on='Country Code', how='left')
years = [str(year) for year in range(2000, 2021)]
df["mean_value"] = df[years].mean(axis=1)

# Titre de l'app
st.title("🌍 Analyse interactive des données éducatives mondiales")

# Sélection d’un indicateur
indicateurs = sorted(df["Indicator Name"].unique())
indicateur = st.selectbox("📊 Choisissez un indicateur", indicateurs)

# Filtrage des données par indicateur
df_filtered = df[df["Indicator Name"] == indicateur]

# Filtrage par région
regions = df_filtered["Region"].dropna().unique()
region = st.selectbox("🌎 Choisissez une région", sorted(regions))
df_region = df_filtered[df_filtered["Region"] == region]

# Graphique des 20 pays avec les plus hautes moyennes
st.subheader(f"Top 20 pays – {indicateur}")
top_countries = df_region.sort_values("mean_value", ascending=False).head(20)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_countries["Country Name"], top_countries["mean_value"], color="teal")
ax.set_xlabel("Valeur moyenne (2000–2020)")
ax.invert_yaxis()
st.pyplot(fig)

# Données brutes
st.subheader("📄 Données sources (aperçu)")
st.dataframe(df_region[["Country Name", "Region", "Income Group", "mean_value"]].sort_values("mean_value", ascending=False))