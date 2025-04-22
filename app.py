

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
#add sidebar title
st.sidebar.header("Filter Options")

#sidebar subheader
st.sidebar.subheader("Year Filter")
#add year range slider with min and max years
minYear = int(df['year'].min())
maxYear = int(df['year'].max())
yearRange = st.sidebar.slider("Year Range", minYear, maxYear, (minYear, maxYear))

#adding mass as input instead of slider as mass goes up to 60million grams so makes slider hard to be precise
#sidebar subheader
st.sidebar.subheader("Mass Filter")
minMass = int(df['mass_g'].min())
maxMass = int(df['mass_g'].max())
st.sidebar.write("Select a mass range (grams):")
min_mass_input = st.sidebar.number_input("Min mass", min_value=minMass, max_value=maxMass, value=minMass, step=100)
max_mass_input = st.sidebar.number_input("Max mass", min_value=minMass, max_value=maxMass, value=maxMass, step=100)

#sidebar subheader for reclass
st.sidebar.subheader("Meteor Class Filters")

#Get a list of all classes that are unique and no NAN
Classes = df['recclass'].dropna().unique()

# Add radio buttons to control which class filter applies
filter_mode = st.sidebar.radio(
    "Class Filter Mode",
    options=["All", "Manual Input"],
    index=0,  # default to "All"
    key="class_mode" # need this to track what option is selected so we can clear the input box when switching to all classes , otherwise it errors 
)

# Clear the input box when all tickbox is selected
if filter_mode == "All" and st.session_state.get("class_input", "") != "":
    st.session_state["class_input"] = ""
    st.rerun()

# If using Manual Input, show dropdown and recomendations of input
if filter_mode == "Manual Input":
    selected_class = st.sidebar.selectbox(
        "Start typing to search for a class",
        options=sorted(Classes),
        index=None,
        placeholder="Type to search...",
          
    )
else:
    selected_class = None


# Filter df based on year
df = df[df['year'].between(yearRange[0], yearRange[1])]
#Filter df based on mass
df = df[df['mass_g'].between(min_mass_input, max_mass_input)]
#filter df based on reclass
if selected_class:
    df = df[df['recclass'] == selected_class]
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
    "html": "<b>Latitude:</b> {reclat} <br/><b>Longitude:</b> {reclong} <br/><b>Name:</b> {name} <br/><b>Year of impact:</b> {year} <br/><b>mass (g):</b> {mass_g} <br/><b>Class (g):</b> {recclass}"
}

# Show map
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))

#endregion
