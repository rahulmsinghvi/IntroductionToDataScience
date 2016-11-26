# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[ ]:

import pandas as pd
import re
import numpy as np
from scipy.stats import ttest_ind

# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[ ]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National',
          'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana',
          'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho',
          'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan',
          'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico',
          'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa',
          'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana',
          'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California',
          'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island',
          'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia',
          'ND': 'North Dakota', 'VA': 'Virginia'}


# In[ ]:




# In[ ]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan","Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State","RegionName"]  )'''
    fname = "../DataFiles/university_towns.txt"
    df = pd.DataFrame()
    with open(fname) as f:
        content = f.readlines()
    for line in content:
        if "[edit]" in line:
            state = line
        else:
            df = df.append(pd.DataFrame({"State": [state], "RegionName": [line]}))
    df['State'] = df['State'].str.replace("\[(.*?)\\n", '')
    df['RegionName'] = df['RegionName'].str.replace("\((.*?)\\n", "").str.rstrip(" ")
    return df


# In[ ]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    df = pd.read_excel("../DataFiles/gdplev.xls", skiprows=7, usecols=range(4, 7))
    df.rename(columns={df.columns.values[0]: 'Quater', df.columns.values[1]: 'GDP', df.columns.values[2]: 'GDPChained'},
              inplace=True)
    df = df[df['Quater'].str.contains('20')]
    df['GDPPreviousChanged'] = df['GDPChained'] - df['GDPChained'].shift(+1)
    df['GDNextChanged'] = df['GDPChained'].shift(-1) - df['GDPChained']
    df['recession'] = (df['GDPPreviousChanged'] < 0) & (df['GDNextChanged'] < 0)
    count = 0
    BottomCount = 0
    for index, row in df.iterrows():
        if ((row['recession'] == True) & (count == 0)):
            recessionStart = row['Quater']
            count += 1
        elif (count > 0):
            if (row['recession'] == True):
                count += 1
            elif (BottomCount == 1):
                recessionBottom = row['Quater']
                count = BottomCount = 0
            else:
                BottomCount += 1
        else:
            count = 0
            BottomCount = 0

    return recessionStart


# In[ ]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    df = pd.read_excel("../DataFiles/gdplev.xls", skiprows=7, usecols=range(4, 7))
    df.rename(columns={df.columns.values[0]: 'Quater', df.columns.values[1]: 'GDP', df.columns.values[2]: 'GDPChained'},
              inplace=True)
    df = df[df['Quater'].str.contains('20')]
    df['GDPPreviousChanged'] = df['GDPChained'] - df['GDPChained'].shift(+1)
    df['GDNextChanged'] = df['GDPChained'].shift(-1) - df['GDPChained']
    df['recession'] = (df['GDPPreviousChanged'] < 0) & (df['GDNextChanged'] < 0)
    count = 0
    FalseCount = 0
    for index, row in df.iterrows():
        if ((row['recession'] == True) & (count == 0)):
            recessionStart = row['Quater']
            count += 1
        elif (row['recession'] == True):
            count += 1
        elif ((count >= 1) & (FalseCount == 0)):
            recessionEnd = row['Quater']
            count = 0
            FalseCount += 1
        elif (FalseCount == 1):
            count = 0
            FalseCount = 0
    return recessionEnd


# In[ ]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    df = pd.read_excel("../DataFiles/gdplev.xls", skiprows=7, usecols=range(4, 7))
    df.rename(columns={df.columns.values[0]: 'Quater', df.columns.values[1]: 'GDP', df.columns.values[2]: 'GDPChained'},
              inplace=True)
    df = df[df['Quater'].str.contains('20')]
    df['GDPPreviousChanged'] = df['GDPChained'] - df['GDPChained'].shift(+1)
    df['GDNextChanged'] = df['GDPChained'].shift(-1) - df['GDPChained']
    df['recession'] = (df['GDPPreviousChanged'] < 0) & (df['GDNextChanged'] < 0)
    count = 0
    FalseCount = 0
    for index, row in df.iterrows():
        if ((row['recession'] == True) & (count == 0)):
            recessionStart = row['Quater']
            count += 1
        elif (row['recession'] == True):
            count += 1
        elif ((count >= 1) & (row['recession'] == False)):
            FalseCount += 1
            if (FalseCount == 3):
                count = FalseCount = 0
                recessionBottom = row['Quater']
    return recessionBottom


# In[ ]:
def assigning_quater(i):
    i = int(i)
    if (i % 3 == 0):
        return str(i / 3)
    else:
        return str((i / 3) + 1)


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df = pd.read_csv("../DataFiles/City_Zhvi_AllHomes.csv")
    df = df.set_index(['State', 'RegionName'])
    df = df.iloc[:, np.r_[0:3, 49:len(df.columns)]]
    df3 = df.ix[:, 0:3]
    df2 = df.ix[:, 3:len(df.columns)]

    for column in df2:
        df2.rename(columns={column: column[0:4] + "q" + assigning_quater(column[5:7])}, inplace=True)

    for column in df2:
        df3[column] = df2[column].mean(axis=1)

    #print(df3.columns.values)
    df3.drop('RegionID', axis=1, inplace=True)
    df3.drop('Metro', axis=1, inplace=True)
    df3.drop('CountyName', axis=1, inplace=True)
    return df3


# In[ ]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)111
    is true or not as well as the p-value of the confidence.
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    reversed_dict = {v: k for k, v in states.iteritems()}

    university_town = get_list_of_university_towns()
    university_town["State"].replace(reversed_dict, inplace=True)
    university_town = university_town.set_index(['State', 'RegionName'])

    housePrices = convert_housing_data_to_quarters()[[get_recession_start(),get_recession_bottom()]].dropna()
    housePrices['Priceratio'] = housePrices[get_recession_start()] / housePrices[get_recession_bottom()]

    univ_values = pd.merge(housePrices, university_town, how='inner', left_index=True, right_index=True)
    non_univ_values = pd.merge(housePrices, university_town, how='left', left_index=True, right_index=True, indicator=True)
    non_univ_values = non_univ_values[non_univ_values['_merge'] == 'left_only']
    univ_values['Priceratio'] = univ_values['Priceratio'].apply(pd.to_numeric)
    non_univ_values['Priceratio'] = non_univ_values['Priceratio'].apply(pd.to_numeric)

    test = ttest_ind(univ_values['Priceratio'], non_univ_values['Priceratio'])

    p = test[1]
    if p < 0.01:
        different=True
    else:
        different=False

    univ_values_mean = univ_values['Priceratio'].mean()
    non_univ_values_mean = non_univ_values['Priceratio'].mean()
    if univ_values_mean < non_univ_values_mean:
        better = univ_values_mean
    else:
        better = non_univ_values_mean

    tuple1 = (different, p, better)
    return tuple1