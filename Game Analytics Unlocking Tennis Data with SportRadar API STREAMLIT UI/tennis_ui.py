import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from data_clean import get_copetitors_data

merged_df=get_copetitors_data()

# Main title 
st.title(":blue[Competitors Analysis]")

# Default value for competitorname 

col1, col2, col3, col4= st.columns(4)
col1.metric("Total competitors" , len(merged_df))
col2.metric("Total countries", merged_df['country'].nunique())
col3.metric("Highest points", merged_df['points'].max())
col4.metric("Lowest points", merged_df['points'].min())

# sidebar compenents 

# title
st.sidebar.title("Analysis")

# rank range variables
min_rank = merged_df['rank'].min() # get the minimum rank
max_rank = merged_df['rank'].max() # get the maximum rank

# input text box for name
competitor_name = st.sidebar.text_input("Search by Competitor Name:")
# rank range slider
rank_min, rank_max = st.sidebar.slider("Filter by rank", min_rank, max_rank, (min_rank, max_rank))

# Analytics options

selectors = st.sidebar.radio('Choose an Data:', [':blue[Filtered Competitors]',':blue[Competitor Details Viewer]', ':blue[Country-Wise Analysis]', ':blue[Leader boards]', ':blue[Country geo view]'])

# filtered dataframe with input name and given rank range
filtered_df=merged_df[merged_df['rank'].between(rank_min,rank_max)]#rank
filtered_competitors_df=filtered_df[filtered_df['name'].str.contains(competitor_name,case=False)]#name


# Filtered Competitors function
def filtered_competitors():
    if competitor_name:
        
        if filtered_competitors_df.empty:
          st.header(":red[No Competitors Found for given filteres]")
        else:
          st.header(":green[Filtered Competitors]")
          st.dataframe(filtered_competitors_df.reset_index(drop=True))
    else:
        st.header(":green[Filtered Competitors]")
        st.dataframe(filtered_df.reset_index(drop=True))

# Competitor Details Viewer function
def competitor_details():
   
   
   if competitor_name:
      print("hi")

      if filtered_competitors_df.empty:
         st.header(":red[No Competitors Found for given filteres]")
      else:
         st.header(":green[Competitors Details Viewer]")
         competitor = st.selectbox("Select Competitor", filtered_competitors_df['name'].unique())
         competitor_info=filtered_competitors_df[filtered_competitors_df['name']==competitor].iloc[0]
         
         st.write(f"***Rank :*** {competitor_info['rank']}")
         st.write(f"***Points :*** {competitor_info['points']}")
         st.write(f"**Movement:** {competitor_info['movement']}")
         st.write(f"***Competition Played :*** {competitor_info['competitions_played']}")
         st.write(f"***Country :*** {competitor_info['country']}")
   else:
       st.header(":green[Competitors Details Viewer]")
       competitor=st.selectbox("Select Competitor",filtered_competitors_df['name'].unique())
       competitor_info=filtered_competitors_df[filtered_competitors_df['name']==competitor].iloc[0]
       
       st.write(f"***Rank :*** {competitor_info['rank']}")
       st.write(f"***Points :*** {competitor_info['points']}")
       st.write(f"**Movement:** {competitor_info['movement']}")
       st.write(f"***Competition Played :*** {competitor_info['competitions_played']}")
       st.write(f"***Country :*** {competitor_info['country']}")

def country_graph():
   country_stats=merged_df.groupby('country').agg(
      Total_Competitors=('name','count'),
      Average_Points=('points','mean'),
   ).reset_index()

   st.header(":green[Country-Wise Analysis]")
   fig=px.bar(
      country_stats,
      x='country',
      y='Total_Competitors',
      color='country',
      title="Number of Competitors by Country",
      text=country_stats['Average_Points']
   )
   st.plotly_chart(fig)

   st.write(country_stats.reset_index(drop=True))

def leader_board():
   st.header(":green[Leader boards]")
   top_ranked=merged_df.sort_values(by='rank').head(5)
   top_points=merged_df.sort_values(by='points',ascending=False).head(5)
   st.write("Top rank competitors")  
   st.dataframe(top_ranked[['name','rank','country']].reset_index(drop=True))
   st.write("Top points competitors")
   st.dataframe(top_points[['name','points','country']].reset_index(drop=True))

def country_geo_graph():
   country_stats=merged_df.groupby(['country','country_code']).agg(
      
      Total_Competitors=('name','count'),
   ).reset_index()
   st.header(":green[Geographical reprensentation of competitors]")


   fig1=px.scatter_geo(
      country_stats,
      locations='country_code',
      color='country',
      hover_name='country',
      size='Total_Competitors',
      #projection='natural earth',
      projection='natural earth',
      title="Number of Competitors by Country",
      #color_continuous_scale=px.colors.sequential.Plasma
      )
 
   st.plotly_chart(fig1)
   st.write(country_stats.sort_values(by='Total_Competitors',ascending=False).reset_index(drop=True))

   

if selectors == ':blue[Filtered Competitors]':
   filtered_competitors()
elif selectors==':blue[Competitor Details Viewer]':
   competitor_details()
elif selectors==':blue[Country-Wise Analysis]':
   country_graph()
elif selectors==':blue[Leader boards]':
   leader_board()
else:
   country_geo_graph()
   
    



   
