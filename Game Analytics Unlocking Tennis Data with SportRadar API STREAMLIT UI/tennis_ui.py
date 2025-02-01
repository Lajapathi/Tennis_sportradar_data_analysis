import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from data_clean import get_copetitors_data

merged_df=get_copetitors_data()
# Sample data (replace with your actual dataset)
print("sucess")

st.title("Competitor Dashboard")

# Homepage Dashboard
total_competitors = len(merged_df)
total_countries = merged_df['country'].nunique()
highest_points = merged_df['points'].max()

# display summary statistics
col1, col2, col3 = st.columns(3)
col1.metric("Total Competitors", total_competitors)
col2.metric("Countries Represented", total_countries)
col3.metric("Highest Points Scored", highest_points)

# search and Filter Competitors for sidebar

st.sidebar.header("Search and Filter Competitors")

# search by competitor name
competitor_name = st.sidebar.text_input("Search by Competitor Name:")

# filter by rank range

rank_range_s=merged_df['rank'].min()
rank_range_e=merged_df['rank'].max()
rank_min, rank_max = st.sidebar.slider("Filter by Rank Range", 1, 500, (rank_range_s, rank_range_e))


# apply filters to the Dataframe

filtered_df = merged_df[
    merged_df['rank'].between(rank_min, rank_max) 
    #merged_df['points'] >= points_min
]

if competitor_name:
    # apply filter if the competitor_name is not empty
    filtered_df = filtered_df[filtered_df['name'].str.contains(competitor_name, case=False)]

    # Check if any competitors are {worng / not found} after filtering
    if filtered_df.empty:
        st.text("No competitor found with the provided name and rank range.")
    else:
    
        st.subheader("Filtered Competitors")
        st.dataframe(filtered_df)
        st.header("Competitor Details Viewer")

        competitor = st.selectbox("Select Competitor", filtered_df['name'])

        # display detailed information about the selected competitor
        
        competitor_info = filtered_df[filtered_df['name'] == competitor].iloc[0]
        st.write(f"**Rank:** {competitor_info['rank']}")
        st.write(f"**Movement:** {competitor_info['movement']}")
        st.write(f"**Competitions Played:** {competitor_info['competitions_played']}")
        st.write(f"**Country:** {competitor_info['country']}")
        st.write(f"**Points:** {competitor_info['points']}")



else:
    
    # If no competitor_name is provided, just show the filtered data
    
    st.subheader("Filtered Competitors")
    st.dataframe(filtered_df)
    st.header("Competitor Details Viewer")

    competitor = st.selectbox("Select Competitor", filtered_df['name'])

    # Display detailed information about competitors
    
    competitor_info = filtered_df[filtered_df['name'] == competitor].iloc[0]
    st.write(f"**Rank:** {competitor_info['rank']}")
    st.write(f"**Movement:** {competitor_info['movement']}")
    st.write(f"**Competitions Played:** {competitor_info['competitions_played']}")
    st.write(f"**Country:** {competitor_info['country']}")
    st.write(f"**Points:** {competitor_info['points']}")

st.header("Country-Wise Analysis")

# group by country and calculate total competitors and average points

country_stats = merged_df.groupby('country').agg(
    Total_Competitors=('name', 'count'),
    Average_Points=('points', 'mean')
).reset_index()

# show country-wise analysis as a table

st.write(country_stats)

# plot bar chart country-wise analysis
fig = px.bar(
    country_stats,
    x='country',
    y='Total_Competitors',
    color='country',
    title="Number of Competitors by Country"
)
st.plotly_chart(fig) # ploting.

# Leaderboards

st.header("Leaderboards")

# Top-ranked competitors

st.subheader("Top Ranked Competitors")
top_ranked = merged_df.sort_values(by='rank').head(5)
st.dataframe(top_ranked[['name', 'rank', 'points']].reset_index(drop=True))

# Competitors with the highest points

st.subheader("Competitors with Highest Points")
top_points = merged_df.sort_values(by='points', ascending=False).head(5)
st.dataframe(top_points[['name', 'rank', 'points']].reset_index(drop=True))
