import streamlit as st
import requests
from streamlit_folium import folium_static
import folium
import pandas as pd
from locationHERE import getCoordinates
from map import make_map
import plotly.graph_objects as go


def app():
	df = pd.read_csv("locData.csv")
	loc = st.text_input('Enter location')
	fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='#273346',
                align='left'),
    cells=dict(values=[df.index,df.location, df.score],
               fill_color='#273346',
               align='left'))
	])
	# fig.update_layout(width = 800)
	st.write(fig)
	# st.table(df)
	if loc:
		coordinates = getCoordinates(loc)
		emp = st.empty()
		with emp.container():
			st.title("Map")
			placeholder_map = st.empty()
			with placeholder_map.container():
				main_map = make_map(coordinates['coordinates'])
				folium_static(main_map)

if __name__ == '__main__':
	app()