import streamlit as st 
import pandas as pd 
import preprocessor , helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy as scipy

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_region_1 (1)')

df = preprocessor.preprocess(df , region_df)

user_menu = st.sidebar.radio(
    'Select an option' , 
    ('medal_tally' , 'Overall Analysis' , 'Country-Wise Analysis' , 'Athlete Wise Analysis' )
    
)


if user_menu == 'medal_tally' : 
    
    st.header('Medal Tally')
    years , country = helper.country_year_list(df)
    
    selected_year = st.sidebar.selectbox('Select Year' , years)
    selected_country = st.sidebar.selectbox('Select Country' , country)
    
    medal_tally  = helper.fetch_medal_tally(df , selected_year , selected_country)
    
    if selected_year == 'overall' and selected_country == 'overall' : 
        st.title('overall analysis')    
        
    if selected_year != 'overall' and selected_country == 'overall' : 
        st.title('Medal Tally in' +" "+  str(selected_year) +" " + "  "+'   olympics')
        
    if selected_year == 'overall' and selected_country != 'overall' : 
        st.title(selected_country + " " + "overall performace")
        
    if selected_year != 'overall' and selected_country != 'overall' : 
        st.title(selected_country + " "+ "performace in" +" "+ str(selected_year) + 'olympics')
        
    st.table(medal_tally)
    


if user_menu == 'Overall Analysis' : 
    
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0] 
    events = df['Event'].unique().shape[0]
    atheletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    
    
    st.title("Top Statistics")
    
    
    col1 , col2 , col3  = st.columns(3)
    
    with col1 : 
        st.header("Editions")
        st.title(editions)
        
    with col2 : 
        st.header("Hosts")
        st.title(cities)
        
    with col3 : 
        st.header("sports")
        st.title(sports)
        
    col1 , col2 , col3  = st.columns(3)
    
    with col1 : 
        st.header("Events")
        st.title(events)
        
    with col2 : 
        st.header("Athelits")
        st.title(atheletes)
        
    with col3 : 
        st.header("nations")
        st.title(nations)
        
        
    nations_over_time = helper.Data_over_time(df , 'region')
    fig = px.line(nations_over_time , x = 'Edition' , y = 'region')
    st.title("participating Nations over the years")
    st.plotly_chart(fig)
    
    nations_over_Event = helper.Data_over_time(df , 'Event')
    fig = px.line(nations_over_Event , x = 'Edition' , y = 'Event')
    st.title("Events over the years")
    st.plotly_chart(fig)
    
    athelete_over_time = helper.Data_over_time(df , 'Name')
    fig = px.line(athelete_over_time , x = 'Edition' , y = 'Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)
    
    
    st.title("No. of Events over time (Every Sport)")
    fig , ax = plt.subplots(figsize=(20 , 20))
    x = df.drop_duplicates(['Year' , 'Sport' , 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport' , columns='Year' , values='Event' , aggfunc='count').fillna(0).astype('int'),annot=True)
    
    st.pyplot(fig)
    
    
    st.title('Most Succesfull Athletes')
    sport = df['Sport'].unique().tolist()
    sport.sort()
    sport.insert(0 , 'overall')
    
    selected_sport = st.selectbox( 'selected_sport' ,sport)
    x = helper.most_successfull_athelit(df , selected_sport)    
    st.table(x)
    
if user_menu == 'Country-Wise Analysis' : 
    
    country = helper.country_list(df)
    
    selected_country = st.selectbox('Select Country' , country)
    
    country_df = helper.year_wise_medal_tally(df , selected_country)
    fig = px.line(country_df , x = 'Year' , y = 'Medal')
    st.title("{} Medal Tally over the years".format(selected_country))
    st.plotly_chart(fig)
    
    
    fig , ax = plt.subplots(figsize=(20 , 20))
    x = helper.country_wise_sport(df , selected_country)
    ax = sns.heatmap(x.pivot_table(index='Sport' , columns='Year' , values='Medal' , aggfunc='count').fillna(0).astype('int'),annot=True)
    
    st.pyplot(fig)
    
    
    athelit = helper.country_most_successfull_athelit(df , selected_country)
    st.table(athelit)
    
    
    
if user_menu == 'Athlete Wise Analysis' : 
    athelit_df = df.drop_duplicates(subset=['Name' , 'region'])
    x1 = athelit_df['Age'].dropna()
    x2 = athelit_df[athelit_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelit_df[athelit_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelit_df[athelit_df['Medal'] == 'Bronze']['Age'].dropna()
    
    fig = ff.create_distplot([x1 , x2 , x3 , x4] , ['age distribution' , 'gold Medalist' , 'silver medalist' , 'Bronze Medalist'] , show_hist = False , show_rug=False)
    
    st.plotly_chart(fig)
    
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athelit_df[athelit_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
        
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)
    
    
    sport = df['Sport'].unique().tolist()
    sport.sort() 
    selected_sport = st.selectbox( 'selected_sport' ,sport)
    temp_df = helper.weight_vs_height(df , selected_sport) 
    fig , ax = plt.subplots()
    ax = sns.scatterplot(data = temp_df , x=temp_df['Weight'] , y=temp_df['Height'] , hue = temp_df['Medal'] , style=temp_df['Sex'] , s=100)
    
    st.pyplot(fig)
    
    
    temp_df = helper.male_vs_female(df)
    fig = px.line(temp_df , x = 'Year' , y = ['Male' , 'female'])
    st.title("WOMEN VS MEN PARTICIPATING OVER THE YEAR")
    st.plotly_chart(fig)
    
    
    
    