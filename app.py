import streamlit as sl
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/dvdmenu/streamlit_demo_app/main/P4-Movie-Ratings.csv')

df.head()

sl.title("Title")
sl.write("Titles are written with 'sl.title('your text')', this is written in 'sl.write()' '")

sl.write(df)



sl.bar_chart(data=df, x='Audience Ratings %', y='Budget (million $)', use_container_width=True)