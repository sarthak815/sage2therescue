import streamlit as st
import requests
from streamlit_folium import folium_static
import folium
import pandas as pd
from locationHERE import getCoordinates
from map import make_map
def app():
	loc = st.text_input('Enter location')
	if loc:
		coordinates = getCoordinates(loc)
		coordinates
		emp = st.empty()
		with emp.container():
			st.title("Map")
			placeholder_map = st.empty()
			with placeholder_map.container():
				main_map = make_map(coordinates['coordinates'])
				folium_static(main_map)
    

if __name__ == '__main__':
	app()