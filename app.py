

import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("Map of Meteor Landings")

#region LOAD DATASET
df = pd.read_csv(r"D:\GitMeteor\Meteorite_Landings.csv")
df.rename(columns={'mass (g)': 'mass_g'}, inplace=True)  # move this here so it's available to sidebar and map
#endregion

#region CLEAN AND FORMAT DATA
df = df.dropna(subset=['year'])
df = df[df['year'] <= pd.Timestamp.now().year]  # remove dates in the future
df['mass_g'] = pd.to_numeric(df['mass_g'], errors='coerce')
df = df.dropna(subset=['mass_g'])
#endregion

#region SETUP SIDEBAR
st.sidebar.header("Filter Options")

minYear = int(df['year'].min())
maxYear = int(df['year'].max())
yearRange = st.sidebar.slider("Year Range", minYear, maxYear, (minYear, maxYear))

minMass = int(df['mass_g'].min())
maxMass = int(df['mass_g'].max())
MassRange = st.sidebar.slider("Mass Range", minMass, maxMass, (minMass, maxMass))

# Filter df based on year
df = df[df['year'].between(yearRange[0], yearRange[1])]
#Filter df based on mass
df = df[df['mass_g'].between(MassRange[0], MassRange[1])]

#endregion

#region SETUP MAP

# Drop rows with missing coordinates 
df = df.dropna(subset=['reclong', 'reclat','GeoLocation'])


# Create Pydeck scatterplot for map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[reclong, reclat]',  
    get_color='[200, 0, 0, 255]',   # Red color,gree,blue ,tranparancy
    get_radius=3000,                        
    pickable=True,
)

# Add view state to center the map  
view_state = pdk.ViewState(
    latitude=df['reclat'].mean(),
    longitude=df['reclong'].mean(),
    zoom=1,
    pitch=0,
)

# Tooltips on map when hovering mouse over
tooltip = {
    "html": "<b>Latitude:</b> {reclat} <br/><b>Longitude:</b> {reclong} <br/><b>Name:</b> {name} <br/><b>Year of impact:</b> {year} <br/><b>mass (g):</b> {mass_g}"
}

# Show map
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))

#endregion
