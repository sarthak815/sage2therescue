import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import numpy as np

@st.cache(hash_funcs={folium.folium.Map: lambda _: None}, allow_output_mutation=True)
def make_map(df):
    main_map = folium.Map(location=(df['Latitude'], df['Longitude']), zoom_start=15)
    return main_map