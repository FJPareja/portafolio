import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Función para contar el número de 1s en cada columna de un DataFrame
def count_ones(df):
    one_counts = df.sum()  # Suma de los valores por columna
    return one_counts

# Cargar datos desde el archivo Excel
xls = pd.ExcelFile("C:/Users/fjpa2/Downloads/sexo_pais_random.xlsx")
years = xls.sheet_names

# Crear dashboard con Streamlit
st.title("Análisis por Nacionalidad")

# Selector para los años
selected_year = st.sidebar.selectbox("Selecciona un año:", years)
df = pd.read_excel(xls, sheet_name=selected_year, header=None)

# Asignar nombres de columnas
countries_row = df.iloc[1]
sex_row = df.iloc[2]
df = df.drop([0, 1, 2])  # Eliminar las tres primeras filas (no contienen datos)
df.columns = countries_row

# Eliminar la primera columna (columna vacía)
df = df.drop(columns=df.columns[0])

# Convertir valores de string a enteros
df = df.astype(int)

# Gráfico de distribución por sexo (Diagrama de anillo)
zero_count = (df == 0).sum().sum()  # Contar el número de 0s en todo el DataFrame
one_count = (df == 1).sum().sum()  # Contar el número de 1s en todo el DataFrame
fig1 = px.pie(names=['Mujer', 'Hombre'], values=[zero_count, one_count], title='Distribución por Sexo')
st.plotly_chart(fig1)

# Graficar la distribución de chilenos y extranjeros
chilenos = df.iloc[:, 2]  # La columna 3 (index 2) contiene la información de chilenos (1) y extranjeros (0)
chilenos_count = chilenos.value_counts()
chilenos_count.index = ['Extranjero', 'Chileno']
fig2 = px.pie(names=chilenos_count.index, values=chilenos_count.values, title='Chilenos vs Extranjeros')
st.plotly_chart(fig2)

# Gráfico de barras con la nacionalidad
nacionalidad_counts = count_ones(df)  # Contar los 1s en cada columna
fig3 = px.bar(x=nacionalidad_counts.index, y=nacionalidad_counts.values, title='Nacionalidad')
st.plotly_chart(fig3)






