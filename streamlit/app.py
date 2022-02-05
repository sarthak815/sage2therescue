import streamlit as st
import requests
from statistics import mean
from streamlit_folium import folium_static
import folium
import pandas as pd
import numpy as np
from locationHERE import getCoordinates, getCoordinates_df
# from map import make_map
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import About
from functions import scrape_and_get


def make_map(df):
	df = df.values
	main_map = folium.Map(location=(df[0][2], df[0][3]), zoom_start=10)
	for i in range(len(df)):
		folium.CircleMarker(location=[df[i][2], df[i][3]],
            tooltip=f"{df[i][0]}",
            fill=True,
            fill_color="blue",
            color=None,
            fill_opacity=1-(df[i][1]/10),
            radius=10*df[i][1],
        ).add_to(main_map)
	return main_map

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
	# df = scrape_and_get(query='Hurricane Harvey')
	# # print(df)
	# dfLoc = getCoordinates_df(df)
	# # print(dfLoc)
	# if dfLoc['status'] == 1:
	# 	df = dfLoc['dataframe']
	# df.dropna(subset = ["Latitude"], inplace=True)
	# print(df)
	emp = st.empty()
	with emp.container():
		st.markdown('''### Engineering rescue services for the right places.''')
		loc = st.text_input('Enter location')
		if st.button('Submit') and loc:
			df = scrape_and_get(query=loc)
			dfLoc = getCoordinates_df(df)
			if dfLoc['status'] == 1:
				df = dfLoc['dataframe']
			df.dropna(subset = ["Latitude"], inplace=True)
			#latitude +-3, Longitude +-3
			df_npy = df.values
			scores = df_npy.T[1]
			indexes = np.argsort(scores)[::-1]
			df_npy = df_npy[indexes]
			df_npy = df_npy[np.abs(df_npy.T[2] - df_npy[0][2])<=3]
			df_npy = df_npy[np.abs(df_npy.T[3] - df_npy[0][3])<=3]
			df = pd.DataFrame(df_npy,columns=df.columns)
			df.drop_duplicates(subset=['Latitude','Longitude'], inplace=True, keep='first')
			table = go.Figure(data=[go.Table(
				header=dict(values=["locations","Sentiment","Latitude","Longitude"],
							fill_color='#273346',
							align='left'),
				cells=dict(values=[df.locations, df.Sentiment,df.Latitude,df.Longitude],
						fill_color='#273346',
						align='left'))
			])
			barChart = px.bar(df,
							y="Sentiment",
							x="locations",
							color='locations')
			st.write(table)
			st.write(barChart)

			empMap = st.empty()
			with empMap.container():
				st.title("Map")
				placeholder_map = st.empty()
				with placeholder_map.container():
					main_map = make_map(df)
					folium_static(main_map)
	if st.sidebar.button('Home'):
		pass
		
	if st.sidebar.button('About'):
		emp.empty()
		About.app()
if __name__ == '__main__':
	app()