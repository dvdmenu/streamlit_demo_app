import streamlit as sl
import pandas as pd

#read data
df = pd.read_csv('https://raw.githubusercontent.com/dvdmenu/streamlit_demo_app/main/P4-Movie-Ratings.csv')

df.head()

sl.title("Insights on Rotten Tomatoes movie data from 2007 to 2011")
sl.write("TBA: Some explanatory stuff")

#this will create a scrollable window for the dataframe
sl.write(df)



sl.bar_chart(data=df, x='Audience Ratings %', y='Budget (million $)', use_container_width=True)



sl.write("Relationship between critic and audience ratings:")
sl.scatter_chart(data=df, x='Rotten Tomatoes Ratings %', y='Audience Ratings %', use_container_width=True)