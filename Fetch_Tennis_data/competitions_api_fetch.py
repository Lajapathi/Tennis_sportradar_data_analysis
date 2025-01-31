import requests
import psycopg2
import csv
import json

api_key = 'nPOXhxzKn6icMsDMnNls7uiAMTnvT9ucaELfllNH'
headers = {'Accept': 'application/json'}

params ={'api_key':api_key}


# api url for cometition and complexes for tennis sport endpoints

competitions_url ='https://api.sportradar.com/tennis/trial/v3/en/competitions.json'


#fecthing the data from the api by {get} request

competitions_response = requests.get(competitions_url, headers=headers, params=params)



if competitions_response.status_code==200: #check http request status code
    competitions_data=competitions_response.json() #convert the response data into json format
else:
    print(f'Error in fetching the data with status code : {competitions_response.status_code}')
    
#### sql connection credentials

connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="laja1103",
    database="Tennis_D"

)

cursor=connection.cursor() 

#### create table query

cursor.execute('''create table if not exists categories_table 
               (category_id varchar(50)Primary key,
               category_name varchar(50) not null)''')

#### inserting data in categories_table

for competition in competitions_data['competitions']:
    category = competition['category']
    
    category['id']=category['id'].replace('sr:category:','') # removing sr:competition from category_id
    
    cursor.execute('''
        INSERT INTO categories_table (category_id, category_name)
        VALUES (%s, %s)
        ON CONFLICT (category_id) DO NOTHING
    ''', (category['id'], category['name']))
    

print("categories_table values inserted successfully")

# inserting data in competitions_table

for competition in competitions_data['competitions']:
    
    competition['id']=competition['id'].replace('sr:competition:','') 
    category = competition['category']
    category['id']=category['id'].replace('sr:category:','')
    
    parent_id = competition.get('parent_id', None) #checking for none
    if parent_id is None:
        parent_id = 'NULL'  # Replace None with 'NULL'
    else:
        parent_id=competition['parent_id'].replace('sr:competition:','') # removing sr:competition from parent_id

    # category = competition['category']
    # category['id']=category['id'].replace('sr:category:','')

    cursor.execute('''
        INSERT INTO competitions_table ( competition_id, competition_name, parent_id, type, gender, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (competition_id) DO NOTHING
     ''', (competition['id'],competition['name'],parent_id,competition['type'],competition['gender'],category['id']))

print("competitions_table values inserted successfully")

connection.commit()



