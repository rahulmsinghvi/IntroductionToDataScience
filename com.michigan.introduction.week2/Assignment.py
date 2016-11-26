
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. Use this dataset to answer the questions below.

# In[1]:

import pandas as pd

df = pd.read_csv('../DataFiles/olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[2]:

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[33]:

def answer_one():
    return df['# Summer'].idxmax()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[4]:

def answer_two():
    typ = df['Gold'].sub(df['Gold.1'])
    df2=pd.DataFrame({'Country':typ.index, 'Difference':typ.values})
    df2 = df2.set_index('Country')
    return df2['Difference'].idxmax()


# ### Question 3
# Which country has the biggest difference between their summer and winter gold medal counts relative to their total gold medal count? Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[6]:

def answer_three():
    df2 = df[(df['Gold']!=0) & (df['Gold.1']!=0)]
    TotalGold = df2['Gold'] + df2['Gold.1']
    Dif = df2['Combined total'] - TotalGold
    df3 = pd.DataFrame({'Country':Dif.index, 'Difference':Dif.values})
    df3 = df3.set_index('Country')
    return df3['Difference'].idxmax()


# ### Question 4
# Write a function to update the dataframe to include a new column called "Points" which is a weighted value where each gold medal counts for 3 points, silver medals for 2 points, and bronze mdeals for 1 point. The function should return only the column (a Series object) which you created.
# 
# *This function should return a Series named `Points` of length 146*

# In[18]:

def answer_four():
    df['Points'] = df['Gold']*3 + df['Silver']*2 + df['Bronze'] + df['Gold.1']*3 + df['Silver.1']*2 + df['Bronze.1']
    df2 = df['Points']
    return df2


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[19]:

census_df = pd.read_csv('../DataFiles/census.csv')
census_df.head()


# In[22]:

def answer_five():
    Dif=census_df.groupby('STNAME')['CTYNAME'].apply(lambda x: len(x.unique()))
    df3 = pd.DataFrame({'State':Dif.index, 'County':Dif.values})
    df3 = df3.set_index('State')
    return df3['County'].idxmax()


# ### Question 6
# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)?
# 
# *This function should return a list of string values.*

# In[26]:

def answer_six():
    TopStates = census_df.groupby('STNAME')['POPESTIMATE2015'].nlargest(3).reset_index(level=1, drop=True)
    Top3 = TopStates.groupby(TopStates.index).sum().nlargest(3)
    return list(Top3)


# ### Question 7
# Which county has had the largest change in population within the five year period (hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all five columns)?
# 
# *This function should return a single string value.*

# In[29]:

def answer_seven():
    Highest = ((census_df2['POPESTIMATE2015']-census_df2['POPESTIMATE2014']))
    Highest2 = Highest.unique
    type(Highest)
    census_df.iloc[28]['STNAME']
    return "YOUR ANSWER HERE"


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[28]:

def answer_eight():
    census_df2 = census_df[(census_df['REGION']==1) | (census_df['REGION']==2)]
    census_df2 = census_df2[census_df2['CTYNAME'].str.contains('Washington')]
    census_df2[['POPESTIMATE2014','POPESTIMATE2015']]=census_df2[['POPESTIMATE2014','POPESTIMATE2015']].apply(pd.to_numeric)
    census_df2 = census_df2[census_df2['POPESTIMATE2015']>census_df2['POPESTIMATE2014']]
    census_df1 = census_df2[['STNAME','CTYNAME']]
    return census_df1
