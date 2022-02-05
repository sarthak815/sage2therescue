import streamlit as st
import requests
from statistics import mean
from streamlit_folium import folium_static
import folium
import pandas as pd
import numpy as np
from locationHERE import getCoordinates, getCoordinates_df
from map import make_map
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import About
from functions import scrape_and_get
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
		if loc:
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
			# for row in df_npy:
			# 	indexes = np.argwhere((df_npy.T[2]==row[2]))
			df = pd.DataFrame(df_npy,columns=df.columns)
			# duplicate_df = df[df.duplicated(['Latitude','Longitude'])]
			# print(duplicate_df)
			# df = df.groupby(['Latitude','Longitude']).agg({'Sentiment':'mean'})
			# df.sort_values(by = ['Latitude','Longitude','Sentiment'], ascending = [False, False, False], inplace=True)
			df.drop_duplicates(subset=['Latitude','Longitude'], inplace=True, keep='first')
			# rowDrop = []
			# meanScore = []
			# i = 0
			# while i < len(df)-1:
			# 	k = i
			# 	scoreM = []
			# 	while df.loc[i, 'Latitude'] == df.loc[k+1, 'Latitude'] and df.loc[i, 'Longitude'] == df.loc[k+1, 'Longitude']:
			# 		scoreM.append(df.loc[k+1,'Sentiment'])
			# 		rowDrop.append(k+1)
			# 		k+=1
			# 	if len(scoreM) > 0:
			# 		scoreVal = mean(scoreM)
			# 	else:
			# 		scoreVal = df.loc[i,'Sentiment']
			# 	meanScore.append(scoreVal)
			# 	i = k
			# df = df.drop(labels=rowDrop, axis=0)
			# df['meanScore'] = meanScore
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