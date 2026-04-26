import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("paris_housing_prices_dataset.csv")
df_encoded = pd.get_dummies(df, columns=["Property_Type", "Condition"], drop_first=True)

x = df_encoded.drop(["Price_EUR", "Property_ID"], axis=1)
y = df_encoded["Price_EUR"]

modelo = LinearRegression()
modelo.fit(x, y)


st.title("Prevendo o valor de casas em Paris")

arrondissement = st.number_input("Bairro (1-20)", 1, 20, 1)
size = st.number_input("Tamanho (m²)", 10, 500, 50)
rooms = st.number_input("Número de Quartos", 1, 10, 2)
floor = st.number_input("Andar", 0, 20, 1)
year = st.number_input("Ano de Construção", 1800, 2025, 1990)
dist = st.number_input("Distância do Centro (km)", 0.0, 50.0, 5.0)


tipo = st.selectbox("Tipo de Propriedade", ["Apartment", "Loft", "Penthouse", "Studio"])
condicao = st.selectbox("Condição", ["Good", "New", "Renovated", "Needs Renovation"])


input_df = pd.DataFrame(0, index=[0], columns=x.columns)

input_df["Arrondissement"] = arrondissement
input_df["Size_sqm"] = size
input_df["Rooms"] = rooms
input_df["Floor"] = floor
input_df["Year_Built"] = year
input_df["Distance_to_Center_km"] = dist

if tipo != "Apartment":
    input_df[f"Property_Type_{tipo}"] = 1
if condicao != "Good":
    input_df[f"Condition_{condicao}"] = 1

if st.button("Estimar Preço"):
    valor_previsto = modelo.predict(input_df)[0]
    st.success(f"O valor previsto é de € {valor_previsto:,.2f}")