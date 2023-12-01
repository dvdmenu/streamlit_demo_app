import streamlit as sl
import pandas as pd

movies = pd.read_excel('https://github.com/dvdmenu/streamlit_demo_app/raw/main/IMDb+Movie+Database%20Project.xlsx')
movies.head(3)

# let's work with a subset of the data for this project
movies = movies[['Title', 'Release Date', 'Genre', 'Country','Rating',
                 'IMDb Score (1-10)', 'Gross Revenue', 'Budget',]]

movies['Release Year'] = movies['Release Date'].dt.year

movies['Release Year'] = movies['Release Year'].astype("int")

movies = movies[movies['Country'] == 'USA']




sl.title("Feature engineering: Adding Yearly Inflation Adjustment to your Pandas Dataframe")
sl.write("Here is a complete procedure of adjusting movie budgets for inflation using World Bank inflation data. Below you can see my example dataset. It is a movie dataset from IMDB where I've filtered out movies produced outside of USA. It has nominal movie budget that we will complement with an Inflation Adjusted Budget.")

sl.write(movies)


# Inflation correction

sl.header("Downloading and applying World Bank Inflation Data to your dataset")
sl.write("You can find directions as comments in the code block below. It is possible to change the orientation of the inflation dataset to a more suitable form before downloading. However, I chose to download it in a raw form and to learn to clean and rearrange the data by coding for a learning experience. Be adviced that a fully working, self-updating Python CPI library exists. If you need daily inflation adjustment, you should look into it. https://pypi.org/project/cpi/") 

sl.write("In this project, AFI feature was executed manually, matching the datasets by Year values. You can apply this procedure to your project, *mutatis mutandis*.")
         

infl = pd.read_csv('https://raw.githubusercontent.com/dvdmenu/streamlit_demo_app/main/inflation_rates.csv')

drop_these = [1,2,3,4,5]
infl = infl.drop(index=drop_these)

drop_columns = ['Series Name', 'Country Name', 'Country Code', 'Series Code']
infl = infl.drop(columns=drop_columns)


melted_infl = pd.melt(infl, var_name='Year', value_name='InflationRate')

melted_infl['Year'] = melted_infl['Year'].str.extract(r'(\d{4})').astype(int)

df = pd.merge(movies, melted_infl, how='inner', left_on='Release Year', right_on='Year')


df['inflation_factor'] = df['InflationRate'] / 100

df['inflation_adjusted_budget'] = df['Budget'] * df['inflation_factor']

df['inflation_adjusted_budget'] = df['inflation_adjusted_budget'].round(2)

df.rename(columns={'inflation_adjusted_budget': 'Budget (AFI)'}, inplace=True)

df.drop('Year', axis=1, inplace=True)

df.drop('Country', axis=1, inplace=True)


#reorder columns
desired_order = ['Title', 'Release Year', 'Genre', 'Rating', 'Budget', 'Budget (AFI)', 'Gross Revenue', 'IMDb Score (1-10)', 'InflationRate', 'inflation_factor', 'Release Date']
df = df[desired_order]


sl.write("Here is the resulting DataFrame head with a new 'Budget (AFI)' column.")

sl.write(df.head())



sl.header("Comparing nominal and Inflation Adjusted Budgets")

which_budget_button = sl.radio(
    "Show:",
    [":Budget Yearly Means", "***Added Inflation Adjusted Yearly Budget Means***"],
    captions = ["Nominal budget Yearly Means", "Nominal budget means and inflation adjusted Yearly Means by CPI index of USA"])


if which_budget_button == ':Budget Yearly Means':
    selected_variable = df.groupby('Release Year').agg({'Budget': 'mean'})
else:
    selected_variable = df.groupby('Release Year').agg({'Budget': 'mean', 'Budget (AFI)': 'mean'})
    

sl.line_chart(selected_variable)

sl.write(selected_variable)




