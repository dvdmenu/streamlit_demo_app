import streamlit as sl
import pandas as pd
import numpy as np

#read data
df = pd.read_csv('https://raw.githubusercontent.com/dvdmenu/streamlit_demo_app/main/P4-Movie-Ratings.csv')


df['Year of release'] = df['Year of release'].astype(str)

df.head()

sl.title("Feature engineering: Adding Yearly Inflation Adjustment to your Pandas Dataframe")
sl.write("Here is a complete procedure of adjusting movie budgets for inflation using World Bank inflation data. Below you can see my example dataset. It is a movie dataset from Rotten Tomatoes 2007-2011. It has nominal movie budget (in million $) that we will complement with an Inflation Adjusted Budget. Altough the unit is one million dollar and not one dollar, the same procedure can be applied to the latter case without any modifications.")

#this will create a scrollable window for the dataframe
sl.write(df)

sl.header("Downloading and applying World Bank Inflation Data to your dataset")
sl.write("You can find directions as comments in the code block below. Be adviced that a fully working, self-updating Python CPI library exists. You should definitely take advantage of it, especially if you need daily inflation adjustment. https://pypi.org/project/cpi/") 

sl.write("In this project, AFI feature was executed manually, matching the datasets by Year values. You can apply this procedure to your project, mutatis mutandis.")
         

code = '''
#  inflation rate chart downloaded from consumer price index, filtered by USA.
# base period 2010 = 100. This means that if 2011 CPI equals 115, prices have gone up 15 % from 2010. 
# link https://databank.worldbank.org/reports.aspx?source=2&series=FP.CPI.TOTL&country=USA#

# remember to export pandas as pd

infl = pd.read_csv('https://raw.githubusercontent.com/dvdmenu/streamlit_demo_app/main/inflation_rates.csv')


# get rid of unnecessary rows and columns
drop_these = [1,2,3,4,5]
infl = infl.drop(index=drop_these)

drop_columns = ['Series Name', 'Country Name', 'Country Code', 'Series Code']
infl = infl.drop(columns=drop_columns)

# pivot inflation table with the beautiful Pandas melt function
melted_infl = pd.melt(infl, var_name='Year', value_name='InflationRate')

# clean unnecessary chars from year column, recode to int
melted_infl['Year'] = melted_infl['Year'].str.extract(r'(\d{4})').astype(int)

# merge dataframes, drop unnecessary double column
df = pd.merge(df, melted_infl, left_on='Year of release', right_on='Year', how='inner')
df.drop('Year', axis=1, inplace=True)

# engineer necessary column for inflation adjusting
# engineer inflation adjusted budget column

df['inflation_factor'] = df['InflationRate'] / 100
df['inflation_adjusted_budget'] = df['Budget (million $)'] * df['inflation_factor']

#reorder columns, uniform column names
desired_order = ['Film', 'Genre', 'Year of release', 'Rotten Tomatoes Ratings %', 'Audience Ratings %', 'Budget (million $)', 'inflation_adjusted_budget', 'InflationRate', 'inflation_factor']
df = df[desired_order]

df.rename(columns={'inflation_adjusted_budget': 'Budget (million $) AFI'}, inplace=True)
df.rename(columns={'InflationRate': 'inflation_rate'}, inplace=True)

'''

sl.code(code, language='python', line_numbers=True)

#  inflation rate chart downloaded from consumer price index, filtered by USA.
# base period 2010 = 100. This means that if 2011 CPI equals 115, prices have gone up 15 % from 2010. 
# link https://databank.worldbank.org/reports.aspx?source=2&series=FP.CPI.TOTL&country=USA#

infl = pd.read_csv('https://raw.githubusercontent.com/dvdmenu/streamlit_demo_app/main/inflation_rates.csv')



# get rid of unnecessary rows and columns
drop_these = [1,2,3,4,5]
infl = infl.drop(index=drop_these)

drop_columns = ['Series Name', 'Country Name', 'Country Code', 'Series Code']
infl = infl.drop(columns=drop_columns)

# pivot inflation table with the beautiful Pandas melt function
melted_infl = pd.melt(infl, var_name='Year', value_name='InflationRate')

# clean unnecessary chars from year column, recode to int
melted_infl['Year'] = melted_infl['Year'].str.extract(r'(\d{4})').astype(str)

# merge dataframes, drop unnecessary double column
df = pd.merge(df, melted_infl, left_on='Year of release', right_on='Year', how='inner')
df.drop('Year', axis=1, inplace=True)

# engineer necessary column for inflation adjusting
# engineer inflation adjusted budget column

df['inflation_factor'] = df['InflationRate'] / 100
df['inflation_adjusted_budget'] = df['Budget (million $)'] * df['inflation_factor']

#reorder columns, uniform column names
desired_order = ['Film', 'Genre', 'Year of release', 'Rotten Tomatoes Ratings %', 'Audience Ratings %', 'Budget (million $)', 'inflation_adjusted_budget', 'InflationRate', 'inflation_factor']
df = df[desired_order]

df.rename(columns={'inflation_adjusted_budget': 'Budget (million $) AFI'}, inplace=True)
df.rename(columns={'InflationRate': 'inflation_rate'}, inplace=True)




sl.write("Here is the resulting DataFrame with a new 'Budget (million $) AFI' column.")

sl.write(df)



sl.header("Comparing nominal and Inflation Adjusted Budgets")

which_budget_button = sl.radio(
    "Show:",
    [":Budget mean (million $)", "***Added Inflation Adjusted Budget mean (million $)***"],
    captions = ["Nominal budget means", "Nominal budget means and inflation adjusted means by yearly CPI index of USA"])


if which_budget_button == ':Budget mean (million $)':
    selected_variable = df.groupby('Year of release').agg({'Budget (million $)': 'mean'})
else:
    selected_variable = df.groupby('Year of release').agg({'Budget (million $)': 'mean', 'Budget (million $) AFI': 'mean'})
    

sl.write(selected_variable)

sl.line_chart(selected_variable)




