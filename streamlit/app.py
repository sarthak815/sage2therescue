import streamlit as st
import requests
from streamlit_folium import folium_static
import folium
import pandas as pd
from locationHERE import getCoordinates
from map import make_map
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import About
def app():
	st.sidebar.image('logo.jpg', use_column_width=500, width=300)
	st.title("Sage Rescuer")
	st.sidebar.title("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;NAVIGATION")
	st.markdown("""
		<style>
		div.stButton > button:first-child {
		height:3em;width:18em;border-radius:10px 10px 10px 10px;
		}
		</style>
	""", unsafe_allow_html=True)
	df = pd.read_csv("locData.csv")
	emp = st.empty()
	with emp.container():
		st.markdown('''### Engineering rescue services for the right places.''')
		loc = st.text_input('Enter location')
		table = go.Figure(data=[go.Table(
			header=dict(values=list(df.columns),
						fill_color='#273346',
						align='left'),
			cells=dict(values=[df.index, df.location, df.score],
					fill_color='#273346',
					align='left'))
		])
		barChart = px.bar(df,
						y="score",
						x="location",
						color='location')
		st.write(table)
		st.write(barChart)
		if loc:
			coordinates = getCoordinates(loc)
			empMap = st.empty()
			with empMap.container():
				st.title("Map")
				placeholder_map = st.empty()
				with placeholder_map.container():
					main_map = make_map(coordinates['coordinates'])
					folium_static(main_map)
	if st.sidebar.button('Home'):
		pass
		
	if st.sidebar.button('About'):
		emp.empty()
		About.app()
if __name__ == '__main__':
	app()