# LA Crime API 10/07/22

import pandas as pd
import requests
#Obtain JSON data using REST query
rest=requests.get('https://data.lacity.org/resource/63jg-8b9z.json?'+
                  '$select=crm_cd_desc,count(dr_no)&'+
                  '$group=crm_cd_desc&'+
                  '$where=weapon_desc="HAND GUN"&'+
                  '$having=count_dr_no>20&'+
                  '$order=count_dr_no desc').json()

print("Number of records in rest query results: ", len(rest))
#Constrct a pandas DataFrame and rename the columns
rest_df = pd.DataFrame.from_records(rest)
rest_df.columns = ['Crime_Description','Crime_cnt']

print("\nCrimes that used hand gun in LA 2010-2019:")
print(rest_df)

#####################

from sodapy import Socrata
#using socrata for URL of the API
client = Socrata("data.lacity.org", None)
#specify endpoint & filtering criteria & specify limit=5000
info = client.get('63jg-8b9z',
                select = 'weapon_desc as Weapon,count(weapon_desc) as Weapon_cnt',
                where = 'date_occ > "2018-12-31"',
                group = 'weapon_desc',
                limit = 5000)
#Constrct a pandas DataFrame
agg_info_df = pd.DataFrame.from_records(info)

print("\nNumber of records in Socrata query:\n",agg_info_df.count())
#convert DF data type to integer to do comparison
agg_info_df.Weapon_cnt=agg_info_df.Weapon_cnt.astype('int')
#using .query() to use records with 'weapon_cnt>100'
gt20_df = agg_info_df.query("Weapon_cnt > 100")
#using .sort to sort in descending order
sorted_info_df = gt20_df.sort_values(by = ['Weapon_cnt'], ascending=False)

#Total weapon count
print("\nWeapons used more than 100 times in 2019 in LA:")
print(sorted_info_df)
Total = sorted_info_df['Weapon_cnt'].sum()
print("Total Weapon count in 2019(used >100 times): ", Total)

#calculate Hand Gun usage rate in 2019
Hand = sorted_info_df.loc[sorted_info_df['Weapon']=='HAND GUN', 'Weapon_cnt'].iloc[0]
handpct = round((Hand/Total)*100,2)
print('Hand Gun use rate in 2019: '+ str(handpct)+'%')

#save DataDrame to JSON
sorted_info_df.to_json("LA_Crime.json",orient="index")


