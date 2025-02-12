import streamlit as st
import pandas as pd

st.write("My first Streamlit app 🎈")

@st.cache_data
def load_data():
  return pd.read_csv("https://github.com/dataprofessor/population-dashboard/raw/master/data/us-population-2010-2019-reshaped.csv", 
                     index_col=0)
  
# Llamamos a la función y asignamos el resultado a df
df = load_data()

# Example 1: Inspect your data 
st.header("1. Inspect the data 🔍")
st.write("`st.data_editor` allows us to display AND edit data")
st.data_editor(df)

# Example 2: A simple bar chart
st.header("2. Get started with a simple bar chart 📊")
st.write("Let's chart the US state population data from the year 2019")
st.bar_chart(df[['year', 'states', 'population']],
             x='states',
             y='population')

# Example 3: Add interactivity to a bar chart
st.header("3. Now make it interactive 🪄")
st.write("It's your turn to select a year")

# Using st.selectbox
selected_year1 = st.selectbox("Select a year",
                             list(df.year.unique())[::-1])

if selected_year1:
    df_selected_year1 = df[df.year == selected_year1]
    # Display chart
    st.bar_chart(df_selected_year1,
                 x='states',
                 y='population')

# Using st.slider
selected_year2 = st.slider("Select a year", 2010, 2019)

if selected_year2:
    df_selected_year2 = df[df.year == selected_year2]
    # Display chart
    st.bar_chart(df_selected_year2,
                 x='states',
                 y='population')

# Using st.number_input
selected_year3 = st.number_input("Enter a year",
                               placeholder="Enter a year from 2010-2019",
                               value=2019)

if selected_year3:
    df_selected_year3 = df[df.year == selected_year3]
    # Display chart
    st.bar_chart(df_selected_year3,
                 x='states',
                 y='population')

# Example 4: Integrate another Python library to create a line chart

import altair as alt 

st.header("4. How about a line chart? 📈")

st.write("Track changes over time")

df_line_chart = df.copy()
df_line_chart['year'] = df_line_chart['year'].astype(str)

c = (
    alt.Chart(df_line_chart)
     .mark_line()
     .encode(x=alt.X('year'),
             y=alt.Y('population'),
             color='states')
)

st.altair_chart(c, use_container_width=True)

# Example 5: Add interactivity to an Altair line chart

st.header("5. Sprinkle in more interactivity 🪄")

st.write("Use `st.multiselect` and `st.slider` for data filter before chart creation")

states = st.multiselect("Pick your states",
                        list(df.states.unique())[::-1],
                        "California")
date_range = st.slider("Pick your date range",
                       2010, 2019,
                       (2010, 2019))

if states:
    chart_data = df[df['states'].isin(states)]
    chart_data = chart_data[chart_data['year'].between(date_range[0], date_range[1])]
    chart_data['year'] = chart_data['year'].astype(str)

    c = (
        alt.Chart(chart_data)
         .mark_line()
         .encode(x=alt.X('year'),
                 y=alt.Y('population'),
                 color='states')
    )

    st.altair_chart(c, use_container_width=True)

# Para ejecutar la aplicación, en la terminal, ejecutar el siguiente comando:	
# streamlit run streamlit_app.py