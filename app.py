

import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt


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

#Setup navigation bar to change pages - added pages as overview page was getting cramped
page = st.sidebar.selectbox(
    "Navigate to:",
    ["Overview", "Charts", "Data Tables"]
)

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

if page == "Overview":

    #region SETUP MAP
    st.title("Map of Meteor Landings")
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

    #region SETUP KPIS 

    #add dashboard header
    st.subheader("Key Statistics")

    #create 4 columns , 1 for each kpi
    kpi1,kpi2,kpi3,kpi4 = st.columns(4)

    #create metric for total meteors and display on column kpi1
    kpi1.metric("Total Meteors",len(df))

    #calculate average mass of meteors
    avgMass = df['mass_g'].mean()
    #create metric for average mass and rounded to whole number and adding a comma , as the mass in grams is way too large to display neatly
    kpi2.metric("Average Mass in grams",f"{avgMass:,.0f}")

    #create metric for Maximum mass
    maxMass = df['mass_g'].max()
    kpi3.metric("Maximum Mass in grams",f"{maxMass:,.0f}")

    #create metric for minumum mass
    minMass = df['mass_g'].min()
    kpi4.metric("Minimum Mass in grams",f"{minMass:,.5f}")

    #endregion

elif page == "Charts":

    #region SETUP CHARTS
    st.title("Data Visualisations")

    #Create  top 10 classes chart
    st.subheader("Top 10 Meteor classes")
    topClasses = df["recclass"].value_counts().sort_values(ascending=False).head(10)
    st.bar_chart(topClasses)

    #Create average mass by year line chart
    st.subheader("Average Mass by Year")
    st.write("You can zoom in or out for a better view")
    avg_mass_by_year = df.groupby(df['year'].astype(int))['mass_g'].mean()
    avg_mass_by_year.index = avg_mass_by_year.index.astype(str)
    st.line_chart(avg_mass_by_year)
    #Create mass by class bar chart 
    st.subheader("Top 5 Heaviest Meteorites by class")
    mass_by_class = df.groupby('recclass')['mass_g'].mean().sort_values(ascending=False).head(10)
    mass_by_class.index = mass_by_class.index.astype(str)
    st.bar_chart(mass_by_class)
    
    #endregion

elif page == "Data Tables":
    
    #add heaviest meteor table
    st.subheader("Top 5 Heaviest Meteorites")
    top_5H = df.sort_values(by='mass_g', ascending=False).head(5)
    top_5H['year'] = top_5H['year'].astype(int).astype(str) #convert year string to remove commas but conver to int first otherwise get trailing 0s like 1920.0
    st.table(top_5H[['name', 'mass_g', ('year'), 'recclass',]])

    #add most common meteor class table
    st.subheader("Top 5 Most Common Meteorite Classes")
    top_classes = df['recclass'].value_counts().head(5)
    top_classes.columns = ['Class', 'Count']
    st.table(top_classes)
