
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# All questions are weighted the same in this assignment. This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable's]`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with parenthesis in their name. Be sure to remove these, e.g. `'Bolivia (Plurinational State of)'` should be `'Bolivia'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[45]:

import pandas as pd
import numpy as np

def answer_one():
    #Energy Indicators excel loading and filtering rows
    energy = pd.read_excel("../DataFiles/Energy Indicators.xls", skiprows=17, usecols=range(2,6))
    energy = energy.ix[0:226]

    #Renaming Columns
    energy.rename(columns={energy.columns.values[0]:'Country', energy.columns.values[1]:'Energy Supply', energy.columns.values[2]:'Energy Supply per Capita', energy.columns.values[3]:'% Renewable\'s'}, inplace=True)

    #Replacing '...' with NaN values
    energy.replace(to_replace='...', value=np.NaN, inplace=True)

    #Converting joules to peta joules
    energy['Energy Supply'] = energy['Energy Supply']*1000000

    #Better readability of dataset for debugging
    pd.set_option('display.max_colwidth', -1)

    #Removing () and integers in Country names
    energy['Country'] = energy['Country'].apply(lambda x: x.split('(')[0])
    energy['Country'] = energy['Country'].apply(lambda x: x.rstrip('1234567890 '))
    #energy = energy.set_index('Country')

    #Renaming Country Values
    SouthKoreaIndex = energy[energy['Country'] == 'Republic of Korea'].index.tolist()
    energy.set_value(SouthKoreaIndex, 'Country', 'South Korea')

    USIndex = energy[energy['Country'] == 'United States of America'].index.tolist()
    energy.set_value(USIndex, 'Country', "United States")

    UKIndex = energy[energy['Country'] == "United Kingdom of Great Britain and Northern Ireland"].index.tolist()
    energy.set_value(UKIndex, 'Country', "United Kingdom")

    HongkongIndex = energy[energy['Country'] == "China, Hong Kong Special Administrative Region"].index.tolist()
    energy.set_value(HongkongIndex, 'Country', "Hong Kong")

    ###################################################################
    #Loading US GDP data
    GDP = pd.read_csv("../DataFiles/world_bank.csv",skiprows=4)

    #Renaming Country values
    SouthKoreaIndex= GDP[GDP['Country Name'] == 'Korea, Rep.'].index.tolist()
    GDP.set_value(SouthKoreaIndex, 'Country Name', 'South Korea')

    IranIndex = GDP[GDP['Country Name'] == 'Iran, Islamic Rep.'].index.tolist()
    GDP.set_value(IranIndex, 'Country Name', 'Iran')

    HongkongIndex = GDP[GDP['Country Name'] == 'Hong Kong SAR, China'].index.tolist()
    GDP.set_value(HongkongIndex, 'Country Name', 'Hong Kong')

    ###################################################################
    #Loading country ranks for Energy and Power Technologies
    ScimEn = pd.read_excel("../DataFiles/scimagojr-3.xlsx",skiprows=0)

    #Merginng Energy, GDP and Ranking Dataset on Country Name Index
    Mergeddf1 = energy.merge(GDP, how='outer', left_on='Country', right_on='Country Name')
    Mergeddf = Mergeddf1.merge(ScimEn, how='outer', left_on='Country', right_on='Country')

    #Filtering the countries ranked 1-15
    df = Mergeddf[(Mergeddf['Rank']>0) & (Mergeddf['Rank']<16)]
    df = df.set_index('Country')

    #Selecting specific columns
    df = df[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable\'s', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    return df


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[2]:

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[48]:

def answer_two():
    #Energy Indicators excel loading and filtering rows
    energy = pd.read_excel("../DataFiles/Energy Indicators.xls", skiprows=17, usecols=range(2,6))
    energy = energy.ix[0:226]

    #Renaming Columns
    energy.rename(columns={energy.columns.values[0]:'Country', energy.columns.values[1]:'Energy Supply', energy.columns.values[2]:'Energy Supply per Capita', energy.columns.values[3]:'% Renewable\'s'}, inplace=True)

    #Replacing '...' with NaN values
    energy.replace(to_replace='...', value=np.NaN, inplace=True)

    #Converting joules to peta joules
    energy['Energy Supply'] = energy['Energy Supply']*1000000

    #Better readability of dataset for debugging
    pd.set_option('display.max_colwidth', -1)

    #Removing () and integers in Country names
    energy['Country'] = energy['Country'].apply(lambda x: x.split('(')[0])
    energy['Country'] = energy['Country'].apply(lambda x: x.rstrip('1234567890 '))
    #energy = energy.set_index('Country')

    #Renaming Country Values
    SouthKoreaIndex = energy[energy['Country'] == 'Republic of Korea'].index.tolist()
    energy.set_value(SouthKoreaIndex, 'Country', 'South Korea')

    USIndex = energy[energy['Country'] == 'United States of America'].index.tolist()
    energy.set_value(USIndex, 'Country', "United States")

    UKIndex = energy[energy['Country'] == "United Kingdom of Great Britain and Northern Ireland"].index.tolist()
    energy.set_value(UKIndex, 'Country', "United Kingdom")

    HongkongIndex = energy[energy['Country'] == "China, Hong Kong Special Administrative Region"].index.tolist()
    energy.set_value(HongkongIndex, 'Country', "Hong Kong")

    ###################################################################
    #Loading US GDP data
    GDP = pd.read_csv("../DataFiles/world_bank.csv",skiprows=4)

    #Renaming Country values
    SouthKoreaIndex= GDP[GDP['Country Name'] == 'Korea, Rep.'].index.tolist()
    GDP.set_value(SouthKoreaIndex, 'Country Name', 'South Korea')

    IranIndex = GDP[GDP['Country Name'] == 'Iran, Islamic Rep.'].index.tolist()
    GDP.set_value(IranIndex, 'Country Name', 'Iran')

    HongkongIndex = GDP[GDP['Country Name'] == 'Hong Kong SAR, China'].index.tolist()
    GDP.set_value(HongkongIndex, 'Country Name', 'Hong Kong')

    ###################################################################
    #Loading country ranks for Energy and Power Technologies
    ScimEn = pd.read_excel("../DataFiles/scimagojr-3.xlsx",skiprows=0)

    #Merginng Energy, GDP and Ranking Dataset on Country Name Index
    Mergeddf1 = energy.merge(GDP, how='outer', left_on='Country', right_on='Country Name')
    Mergeddf = Mergeddf1.merge(ScimEn, how='outer', left_on='Country', right_on='Country')

    #Filtering the countries ranked 1-15
    df = Mergeddf[(Mergeddf['Rank']>0) & (Mergeddf['Rank']<16)]
    df = df.set_index('Country')

    #Selecting specific columns
    df = df[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable\'s', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    difference = len(Mergeddf.index)-len(df)
    return difference


# ### Question 3 (6.6%)
# What are the top 15 countries for average GDP over the last 10 years?
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[12]:

def answer_three():
    df = answer_one()
    avgGDP = df[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].mean(axis=1)
    avgGDP.sort_values(ascending=False, inplace=True)    
    return avgGDP


# In[15]:

### Question 4 (6.6%)
#By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?

#*This function should return a single number.*


# In[20]:

def answer_four():
    df = answer_one()
    avgGDP = df[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].mean(axis=1)
    avgGDP.sort_values(inplace=True)
    return avgGDP.values[5]


# ### Question 5 (6.6%)
# What is the mean energy supply per capita?
# 
# *This function should return a single number.*

# In[19]:

def answer_five():
    df = answer_one()
    return df['Energy Supply per Capita'].mean()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[24]:

def answer_six():
    df = answer_one()
    Renewable=df['% Renewable\'s'].max()
    Country=df['% Renewable\'s'].idxmax()
    tuple1 = (Country, Renewable)
    return tuple1


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[26]:

def answer_seven():
    df = answer_one()
    new_df = df.copy()
    new_df['Ratio'] = new_df['Citations']/new_df['Self-citations']
    Ratio=new_df['Ratio'].max()
    Country=new_df['Ratio'].idxmax()
    tuple1 = (Country, Ratio)
    return tuple1

answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[28]:

def answer_eight():
    df = answer_one()
    df['Population'] = df['Energy Supply']/df['Energy Supply per Capita']
    new_df2 = df['Population'].copy()
    new_df2.sort_values(ascending=False,inplace=True)
    return new_df2.index[2]


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita?
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita).*

# In[31]:

def answer_nine():
    df = answer_one()
    df['Citable Documents per person'] = df['Citable documents']/df['Population']
    number = np.correlate(df["Citable Documents per person"], df["Energy Supply per Capita"])
    return number[0]

answer_nine()


# In[32]:

def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# In[33]:

plot9()


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[35]:

def answer_ten():
    df = answer_one()
    median = df['% Renewable\'s'].median()
    HighRenew = df.copy()
    HighRenew['HighRenew'] = 0
    for index, row in HighRenew.iterrows():
        if row['% Renewable\'s'] > median:
            HighRenew.loc[index,'HighRenew'] = 1
    return type(HighRenew)

answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[39]:

ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

def answer_eleven():
    df2 = answer_one()
    df2.reset_index(inplace=True)
    df2["Continent"] = df2['Country'].map(ContinentDict)
    df2.set_index('Country',inplace=True)
    df2.head()
    df2['Population'] = df2['Energy Supply']/df2['Energy Supply per Capita']
    df2

    size = df2.groupby('Continent').size()
    mean = df2.groupby('Continent')['Population'].mean()
    sum1 = df2.groupby('Continent')['Population'].sum()
    std = df2.groupby('Continent')['Population'].std()
    continent = pd.DataFrame({'size':size, 'mean':mean, 'sum':sum1, 'std':std}).fillna(0)    
    return continent


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a Series with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[41]:

def answer_twelve():
    df2 = answer_one()
    RenewableBins = pd.cut(df2['% Renewable\'s'],5)
    df2['Renewable Bins'] = RenewableBins
    return df2.groupby(['Continent','Renewable Bins']).size().dropna()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas)
# 
# e.g. 12345678.90 -> 12,345,678.90
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[44]:

def sample_function(item):
    item = repr(round(item,2))
    pos_of_decimal_point = item.index('.')
    remainder = pos_of_decimal_point % 3
    remainder2 = pos_of_decimal_point % 2
    
    if (remainder == 0):
        if (remainder2 == 0):
            start_position = 1
        else:
            start_position = 2
    elif (remainder == 1):        
        start_position = 2
    else:
        start_position = 1
    
    num_of_braces = int(pos_of_decimal_point/2 - 1)
    count=0
    
    while(count<num_of_braces):
        pos_of_decimal_point = pos_of_decimal_point+1
        append_string = item[start_position:]
        initial_string = item[:start_position]
        item = initial_string + ',' + append_string
        count+=1
        start_position= 2+start_position+1   
            
    return item

def answer_thirteen():
    df2 = answer_one()
    x = df2['Population']
    x = x.reset_index()
    x.columns = ['Country', 'Population']
    x.set_index('Country', inplace=True)
    x['Population'] = x['Population'].apply(sample_function)
    return x['Population']

answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[17]:

def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[18]:

#plot_optional()

