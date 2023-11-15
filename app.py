import streamlit as sl
import pandas as pd

#read data
df = pd.read_csv('https://raw.githubusercontent.com/dvdmenu/streamlit_demo_app/main/P4-Movie-Ratings.csv')

df.head()

sl.title("Insights: Rotten Tomatoes Movie Data from 2007 to 2011")
sl.write("TBA: Some explanatory stuff")

#this will create a scrollable window for the dataframe
sl.write(df)

sl.header("Feature engineering: Adding Yearly Inflation Correction to your Pandas Dataframe")
sl.write("Here is a complete procedure of adjusting movie budgets for inflation using World Bank inflation data. Be adviced that a fully working, self-updating Python CPI library exists. You should definitely take advantage of it. https://pypi.org/project/cpi/ \n In this project, AFI feature was executed manually for learning experience. You can apply this procedure to your project, mutatis mutandis.")

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

sl.write(df)




# --------

# bar chart on audience ratings compared to budget
# sl.bar_chart(data=df, x='Audience Ratings %', y='Budget (million $)', use_container_width=True)


sl.write("Relationship between critic and audience ratings:")

# scatter plot that examines the rating relationship. Needs regression line and P-tests values.
sl.scatter_chart(data=df, x='Rotten Tomatoes Ratings %', y='Audience Ratings %', use_container_width=True)





