import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

# Load the Mumbai population density data as a GeoDataFrame
data_url = "gadm41_IND_1.json"
mumbai_pop_density = gpd.read_file(data_url)

# Define the address and coordinates of HDB branches in Mumbai
hdb_branches = {
    "Fort": (18.937727, 72.836177),
    "Dahisar (East)": (19.248766, 72.867897),
    "Lower Parel": (18.996671, 72.830057),
    "Borivali (West)": (19.229571, 72.847081),
    "Malad (West)": (19.186149, 72.836934),
    "Sakinaka, Andheri (East)": (19.098489, 72.892977),
    "Kalbadevi": (18.950147, 72.829813),
    "Chembur (East)": (19.051519, 72.896424),
    "Kandivali (East)": (19.205711, 72.867565),
    "Bhandup (West)": (19.142536, 72.935260),
    "Goregaon (West)": (19.163850, 72.841319),
    "Ghatkopar (East)": (19.085751, 72.908543),
    "Bhavya Plaza, Khar (West)": (19.070745, 72.837499),
    "Wilson House, Andheri (East)": (19.126697, 72.849045),
    "Tardeo, Mumbai Central": (18.975600, 72.808690),
}

# Set the initial map view to Mumbai
initial_location = (19.0760, 72.8777)
zoom_level = 10

# Create a Leafmap foliumap
m = leafmap.Map(center=initial_location, zoom=zoom_level)

# Add the population density layer to the map
m.add_geojson(mumbai_pop_density, layer_name="Population Density", fill_opacity=0.7, fill_color="YlOrRd")

# Add markers for HDB branches
for branch, coordinates in hdb_branches.items():
    marker = leafmap.Marker(location=coordinates, popup=branch)
    m.add_layer(marker)

# Create a sidebar for user interaction
st.sidebar.title("Mumbai Population Density Map")
radius = st.sidebar.slider("Zoom Radius", min_value=100, max_value=1000, value=500, step=100)
search_place = st.sidebar.text_input("Search for a place in Mumbai")
search_button = st.sidebar.button("Search")

# Zoom the map to the specified radius
if radius:
    m.set_zoom_radius(radius)

# Search for a place in Mumbai and center the map on the location
if search_button:
    place_location = geocode(search_place)
    if place_location:
        m.center = place_location
        m.zoom = 14
    else:
        st.sidebar.warning("Place not found.")

# Display the map
m.to_streamlit()


