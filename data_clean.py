from database_conn import get_db_data
import pandas as pd

session,competitors_table,competitor_rankings_table=get_db_data()

competitors_data = session.query(competitors_table).all()
rankings_data = session.query(competitor_rankings_table).all()

##

competitors_df = pd.DataFrame([{
    'competitor_id': c.competitor_id,
    'name': c.name,
    'country': c.country,
    'country_code': c.country_code,
    'abbreviation': c.abbreviation
} for c in competitors_data])

rankings_df = pd.DataFrame([{
    'rank': r.rank,
    'movement': r.movement,
    'points': r.points,
    'competitions_played': r.competitions_played,
    'competitor_id': r.competitor_id
} for r in rankings_data])

# Merge the two DataFrames based on the competitor_id
merged_df = pd.merge(competitors_df, rankings_df, on='competitor_id', how='inner')

def get_copetitors_data():# function merged_data
    return merged_df
