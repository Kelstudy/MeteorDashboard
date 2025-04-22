import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("Map of NYPD Arrests")

# Load and clean data
df = pd.read_csv(r"C:\Users\Kelvi\OneDrive\Desktop\uni\year2\Sem2\Data Project Lifecycle\CW\individual cw\Meteorite_Landings.csv")

# Drop rows with missing coordinates
df = df.dropna(subset=['Latitude', 'Longitude'])

# Create Pydeck scatterplot
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[Longitude, Latitude]',  
    get_color='[200, 0, 0, 255]',   # Red color,gree,blue ,tranparancy
    get_radius=100,                        
    pickable=True,
)

# Optional: Add view state to center the map nicely
view_state = pdk.ViewState(
    latitude=df['Latitude'].mean(),
    longitude=df['Longitude'].mean(),
    zoom=10,
    pitch=0,
)

# Tooltip showing coordinates on hover
tooltip = {
    "html": "<b>Latitude:</b> {Latitude} <br/><b>Longitude:</b> {Longitude}"
}

# Show map
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))
