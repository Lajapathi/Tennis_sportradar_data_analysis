import requests
import psycopg2

doubles_competitor_rankings_url='https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json'

api_key='nPOXhxzKn6icMsDMnNls7uiAMTnvT9ucaELfllNH'
params ={'api_key':api_key}
headers={'Accept':'application/json'}

doubles_competitor_rankings_response=requests.get(doubles_competitor_rankings_url,headers=headers,params=params)

if doubles_competitor_rankings_response.status_code==200:
    doubles_competitor_rankings_data=doubles_competitor_rankings_response.json() # doubles_competitor_rankings json data
else:
    print(f'doubles_competitor_rankings api error with status_code: {doubles_competitor_rankings_response.status_code}')



print('sucess')

competitor_rankings_list=[]
competitors_list=[]

for i in range(0,len(doubles_competitor_rankings_data['rankings'])):
    for competitor_rankings in doubles_competitor_rankings_data['rankings'][i]['competitor_rankings']:
        
        competitor=competitor_rankings.get('competitor',None)
        
        if competitor is not None: # proceed if competitor is not None
            competitor_rankings_dict={
            
            'rank':competitor_rankings.get('rank'),
            'movement':competitor_rankings['movement'],
            'points':competitor_rankings['points'],
            'competitions_played':competitor_rankings['competitions_played'],
            'competitor_id':competitor['id'].replace('sr:competitor:','')
            }
            
            competitor_rankings_list.append(competitor_rankings_dict) ## complete competitor_rankings data to list
             
            for ele in competitor:
                 
                 #Neutral country_code='N'
                 if competitor['country']=='Neutral':
                     
                     country_code=competitor.get('country_code','N')
                 else:
                     country_code=competitor.get('country_code')
                 #print(competitor['country'])
                 competitors_dict={
                'competitor_id':competitor['id'].replace('sr:competitor:',''),
                'name':competitor['name'],#.replace('-',', ')
                'country':competitor['country'],
                'country_code':country_code,
                'abbreviation':competitor['abbreviation']
                }
                 competitors_list.append(competitors_dict)## complete competitor data to list



## UNIQUE COMPETITORS TO LIST

competitors_UList=[]
seen_competitors_id=set()

for elements in competitors_list:
    if elements['competitor_id'] not in seen_competitors_id:
        competitors_UList.append(elements) # competitors unique list
        seen_competitors_id.add(elements['competitor_id'])
        

## UNIQUE RANKING ELEMENTS TO LIST

competitor_rankings_UList=[]
seen_competitor_rankings_id=set()

for elements in competitor_rankings_list:
    if elements['rank'] not in seen_competitor_rankings_id:
        competitor_rankings_UList.append(elements) # unique competitor_rankings list

#### Database connection

connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="laja1103",
    database="Tennis_D"

)

cursor=connection.cursor() 


for competitors in competitors_UList:
    
    cursor.execute('''
        INSERT INTO competitors_table (competitor_id, name,country,country_code,abbreviation)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (competitor_id) DO NOTHING
    ''', (competitors['competitor_id'], competitors['name'], competitors['country'], competitors['country_code'], competitors['abbreviation']))


print("competitors_table values inserted successfully")



for ranking in competitor_rankings_UList:

    cursor.execute('''
        INSERT INTO competitor_rankings_table (rank,movement,points,competitions_played,competitor_id)
        VALUES (%s, %s, %s, %s, %s)
        
    ''', (ranking['rank'],ranking['movement'], ranking['points'],ranking['competitions_played'],ranking['competitor_id']))


print('competitor_rankings_table values inserted successfully')

connection.commit()