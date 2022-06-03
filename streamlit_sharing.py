import streamlit as st
from multipage import MultiPage
from apps import home_app, vehicles, rural_hub_app, urban_community_hub_app, urban_multimodal_hub_app, commercial_dominant_hub_app

# Create an instance of the app
app = MultiPage()
st.set_page_config(layout="wide")
st.title("Hub Modeling")

#Add all applications here
#app.add_page("Upload Data", home_app.app)
app.add_page("Overview", home_app.app)
app.add_page("Rural Hub", rural_hub_app.app)
app.add_page("Urban Community Hub", urban_community_hub_app.app)
app.add_page("Urban Multimodal Hub", urban_multimodal_hub_app.app)
app.add_page("Commercial Dominant Hub", commercial_dominant_hub_app.app)
app.add_page("Vehicle Info", vehicles.app)

# The main app
app.run()


