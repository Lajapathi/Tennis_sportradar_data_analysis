import requests
import psycopg2
import streamlit as st
import pandas as pd
complexes_url ='https://api.sportradar.com/tennis/trial/v3/en/complexes.json'
api_key='nPOXhxzKn6icMsDMnNls7uiAMTnvT9ucaELfllNH'
params ={'api_key':api_key}
headers={'Accept':'application/json'}

complexes_response=requests.get(complexes_url,headers=headers,params=params)

if complexes_response.status_code==200 :
    complexes_data=complexes_response.json()
else:
    print("Error in api")

complexes_data_list=[]
venues_list=[]

for comp in complexes_data['complexes']:
    complexes_data_dict={
        'complex_id':comp['id'].replace('sr:complex:',''),
        'complex_name':comp['name']
    }
    complexes_data_list.append(complexes_data_dict) ## complete complexes data to list


    vanues=comp.get('venues',None)
    if vanues is not None:
        for venue in vanues:
            venues_data_dict={
                
                'venue_id':venue['id'].replace('sr:venue:',''),
                'venue_name':venue['name'],
                'city_name':venue['city_name'],
                'country_name':venue['country_name'],
                'country_code':venue['country_code'],
                'timezone':venue['timezone'],
                'complex_id':comp['id'].replace('sr:complex:','')}
        
            venues_list.append(venues_data_dict) ## complete venues data to list


## UNIQUE COMPLEXES ELEMENTS TO LIST

complexes_data_UList=[]
seen_complexes_id=set()
for elements in complexes_data_list:
    if elements['complex_id'] not in seen_complexes_id:
        complexes_data_UList.append(elements)
        seen_complexes_id.add(elements['complex_id'])


#### Database connection

connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="laja1103",
    database="Tennis_D"

)

cursor=connection.cursor() 

for complex in complexes_data_UList:
    
    cursor.execute('''
        INSERT INTO complexes_table (complex_id, complex_name)
        VALUES (%s, %s)
        ON CONFLICT (complex_id) DO NOTHING
    ''', (complex['complex_id'], complex['complex_name']))

print("complexes_table values inserted successfully")

for venue in venues_list:
    cursor.execute('''
        INSERT INTO venues_table (venue_id, venue_name, city_name, country_name, country_code,timezone,complex_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (venue_id) DO NOTHING
    ''', (venue['venue_id'], venue['venue_name'], venue['city_name'], venue['country_name'], venue['country_code'], venue['timezone'], venue['complex_id']))

print("venues_table values inserted successfully")


connection.commit()

