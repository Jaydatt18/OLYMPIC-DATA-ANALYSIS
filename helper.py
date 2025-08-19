import numpy as np 
import pandas as pd 

def medal_tally(df): 
    medal_tally = df.drop_duplicates(subset=['Team' , 'NOC' , 'Games' , 'Year' , 'City' , 'Sport' , 'Event' , 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold' , 'Silver' , 'Bronze']].sort_values(by = 'Gold' , ascending=False).reset_index()
    
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    return medal_tally    

def country_year_list(df) : 
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0 , 'overall')
    
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0 , 'overall')
    
    return years , country


# some problem with year and overall analysis 
def fetch_medal_tally(df ,year, country) : 

  medal_df = df.drop_duplicates(subset=['Team' , 'NOC' , 'Games' , 'Year' , 'City' , 'Sport' , 'Event' , 'Medal'])
  flag = 0 
  if year == 'overall' and country == 'overall' :
    temp_df = medal_df
  
  if year == 'overall' and country != 'overall' : 
    flag = 1
    temp_df = medal_df[medal_df['region'] == country]

  if year != 'overall' and country == 'overall' : 
    temp_df = medal_df[medal_df['Year'] == int(year)]

  if year != 'overall' and country != 'overall' : 
    temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

  if flag == 1: 
    x = temp_df.groupby('Year').sum()[['Gold' , 'Silver' , 'Bronze']].sort_values('Gold' , ascending=True).reset_index()
  else: 
    x = temp_df.groupby('region').sum()[['Gold' , 'Silver' , 'Bronze']].sort_values('Gold' , ascending=False).reset_index()
  x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

  return x


#overall analysis Participating natinon overall year

def Data_over_time(df , col):
   nations_over_time = df.drop_duplicates(['Year' , col])['Year'].value_counts().reset_index().sort_values(by='Year')
    
   nations_over_time.rename(
        columns={
        'Year' : 'Edition' , 
        'count' : col
        } 
        , inplace= True
    )
   return nations_over_time
 
 
 
def most_successfull_athelit(df , sport):
  temp_df = df.dropna(subset=['Medal'])

  if sport != 'overall' :
    temp_df = temp_df[temp_df['Sport'] == sport]

  x = temp_df['Name'].value_counts().reset_index().head(10).merge(df , left_on = 'Name' , right_on = 'Name')[['Name' ,'count', 'Sport' , 'region']].drop_duplicates().reset_index()
  x.rename(columns = {
      'Name' : 'Athlete Name' ,
      'count' : 'medal'
  } , inplace = True)

  x.drop(columns = ['index'] , inplace=True)
  x.sort_values

  return x


def year_wise_medal_tally(df , country):
  temp_df = df.dropna(subset=['Medal'])
  temp_df.drop_duplicates(subset=['Team' , 'NOC' , 'Games' , 'Year' , 'City' , 'Sport' , 'Event' , 'Medal'] , inplace=True) 
  
  new_df = temp_df[temp_df['region'] == country ]
  final_df = new_df.groupby('Year').count()['Medal'].reset_index() 
  
  return final_df 


def country_list(df): 
  country = np.unique(df['region'].dropna().values).tolist()
  country.sort()
    
  return country

def country_wise_sport(df , country): 
  temp_df = df.dropna(subset=['Medal'])
  temp_df.drop_duplicates(subset=['Team' , 'NOC' , 'Games' , 'Year' , 'City' , 'Sport' , 'Event' , 'Medal'] , inplace=True) 
  
  new_df = temp_df[temp_df['region'] == country]
  
  return new_df
    
    
def country_most_successfull_athelit(df , country):
  temp_df = df.dropna(subset=['Medal'])

  
  temp_df = temp_df[temp_df['region'] == country]

  x = temp_df['Name'].value_counts().reset_index().head(10).merge(df , left_on = 'Name' , right_on = 'Name')[['Name' ,'count', 'Sport']].drop_duplicates().reset_index()
  x.rename(columns = {
      'Name' : 'Athlete Name' ,
      'count' : 'medal'
  } , inplace = True)

  x.drop(columns = ['index'] , inplace=True)
  x.sort_values

  return x

def weight_vs_height(df , sport): 
  athelit_df  = df.drop_duplicates(subset=['Name' , 'region'])
  athelit_df['Medal'].fillna('No Medal' , inplace=True)
  
  temp_df = athelit_df[athelit_df["Sport"] == sport]
  
  return temp_df


def male_vs_female(df):
  
  athelit_df  = df.drop_duplicates(subset=['Name' , 'region'])
  male = athelit_df[athelit_df['Sex'] == 'M'].groupby('Year')['Name'].count().reset_index()
  female = athelit_df[athelit_df['Sex'] == 'F'].groupby('Year')['Name'].count().reset_index()
  
  final = male.merge(female, on= 'Year')
  final.rename(columns={
    'Name_x' : 'Male' , 
    'Name_y' : 'female'
  } , inplace = True)


  return final 
  
  
  
