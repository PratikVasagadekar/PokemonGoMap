#!/usr/bin/env python3
import pandas as pd
from datetime import datetime, timedelta,timezone
import requests
import json
import time
import pytz
from urllib.parse import quote

class parseMapData:

    def __init__(self, maplocation="nyc"):
        self.maplocation = maplocation

    def fetchMapData(self):
        url = f"{self.maplocation}/query2.php?mons=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605,606,607,608,609,610,611,612,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629,630,631,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695,696,697,698,699,700,701,702,703,704,705,706,707,708,709,710,711,712,713,714,715,716,717,718,719,720,721,722,723,725,726,728,729,731,734,736,737,738,739,741,742,744,747,751,752,753,755,759,761,762,763,764,765,766,767,768,769,770,775,776,777,779,782,785,786,787,788,790,793,794,795,796,797,798,799,803,804,805,806,819,820,831,832,863,870,888,889,894,895,900,906,907,908,909,910,911,912,913,914,915,916,919,920,921,922,923,928,929,930,962,971,972,996,997,998&since=0" 
        headers = {'Referer': f'https://{self.maplocation}/'}
        response_json = {}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            dfResponse = pd.DataFrame(response_json.get('pokemons', []))
            #* Drop rows if the cp is negative
            dfResponse = dfResponse.query("cp != -1")
            #* Drop Columns 
            self.dfMapData = dfResponse.drop(columns=['move1', 'move2', 'costume', 'gender', 'form'])
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
            return None
        return self.dfMapData

    def updatePokemonCPMValues(self):
        #* Read Pokemon Data and merge with NYC Map
        df = pd.read_excel('app/internal/Data/CP Multiplier.xlsx')
        df['Level'] = df['Level'].astype(float)
        self.dfMapData['level'] = self.dfMapData['level'].astype(float)
        self.dfMapData = pd.merge(self.dfMapData, df, left_on='level', right_on='Level', how='left')
        return self.dfMapData

    def updatePokemonNatDexInfo(self):
        #* Read Pokemon Data and merge with NYC Map
        df = pd.read_excel('app/internal/Data/Pokemon Stats.xlsx')
        df = df.drop_duplicates(subset=['National Dex'])
        self.dfMapData = pd.merge(self.dfMapData, df, left_on='pokemon_id', right_on='National Dex', how='left')
        return self.dfMapData

    def CalculateMaxCPByCurIV(self,row):
        attack_iv = row['attack']
        defense_iv = row['defence']
        stamina_iv = row['stamina']
        base_attack = row['Base Attack']
        base_defense = row['Base Defense']
        base_stamina = row['Base Stamina']
        cp_multiplier = 0.8003 #* Level 42
        cp = ((base_attack + attack_iv) * 
            (base_defense + defense_iv)**0.5 * 
            (base_stamina + stamina_iv)**0.5 * 
            cp_multiplier**2) / 10
        return max(cp, 10)

    def CalculateIV(self,row):
        attack_iv = row['attack']
        defense_iv = row['defence']
        stamina_iv = row['stamina']
        max_iv = 45
        iv_percentage = ((attack_iv + defense_iv + stamina_iv) / max_iv) * 100
        return iv_percentage

    def splitTypesColumn(self):
        self.dfMapData[['Primary Type', 'Secondary Type']] = self.dfMapData['Types'].str.split(', ', expand=True)
        self.dfMapData.drop('Types', axis=1, inplace=True)
        return self.dfMapData

    def DropColumns(self,df, columns_to_drop):
        return df.drop(columns=columns_to_drop, errors='ignore').reset_index(drop=True)

    def CalculateRemainingTime(self,target_timestamp):
        india_tz = timezone(timedelta(hours=5, minutes=30))
        current_timestamp = int(datetime.now(india_tz).timestamp())
        remaining_seconds = target_timestamp - current_timestamp
        if remaining_seconds < 0:return "Expired"
        minutes, seconds = divmod(remaining_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def ReArrangeCols(self,df, new_column_order):
        valid_columns = [col for col in new_column_order if col in df.columns]
        return df[valid_columns]

    def getGoogleMapLinks(self):
        self.dfMapData['Google Maps Link'] = self.dfMapData.apply(lambda row: f"https://www.google.com/maps/?q={row['lat']},{row['lng']}", axis=1)
        return self.dfMapData

    def UpdatePokemonImages(self):
        self.dfRaids['Pokemon Image'] = self.dfRaids['Name'].apply(lambda x: f"https://raw.githubusercontent.com/PratikVasagadekar/PokemonGoAssets/main/Images/{quote(x)}.png")
        self.dfMapData['Primary Type'] = self.dfMapData.apply(lambda row: f"https://raw.githubusercontent.com/PratikVasagadekar/PokemonGoAssets/main/Types/{row['Primary Type']}.png", axis=1)
        self.dfMapData['Secondary Type'] = self.dfMapData.apply(lambda row: None if row['Secondary Type'] is None else f"https://raw.githubusercontent.com/PratikVasagadekar/PokemonGoAssets/main/Types/{row['Secondary Type']}.png", axis=1)
        return self.dfMapData


    def ProcessMapData(self):
        #* Get Pokemon Live PoGo Data
        self.fetchMapData()
        #* Add Pokemon Stats Information
        self.updatePokemonNatDexInfo()
        #* Add Pokemon CPM Multipliers
        self.updatePokemonCPMValues()
        #* Update Google Maps Links
        self.dfMapData = self.getGoogleMapLinks()
        #* Split Pokemon types
        self.dfMapData = self.splitTypesColumn()
        #* Update Pokemon Images
        self.dfMapData = self.UpdatePokemonImages()
        #* Apply the function to the dataframe
        self.dfMapData['MAX CP (IV)'] = self.dfMapData.apply(lambda row: self.CalculateMaxCPByCurIV(row), axis=1).round()
        #* Apply the function to the dataframe
        self.dfMapData['IV'] = self.dfMapData.apply(lambda row: self.CalculateIV(row), axis=1).round()
        #* Apply the function to the dataframe to calculate Remaining Time.
        self.dfMapData['Remaining Time'] = self.dfMapData['despawn'].apply(lambda row: self.CalculateRemainingTime(row))
        #* Remove Expired Time mons
        self.dfMapData = self.dfMapData[self.dfMapData['Remaining Time'] != 'Expired']
        #* Drop Unwanted Columns.
        self.dfMapData = self.DropColumns(self.dfMapData, [
            'attack', 'defence', 'stamina', 
            'Max CP', 'Base Attack', 'Base Defense', 'Base Stamina',
            'Weather Boost', 'Catch Rewards', 'Additional Move Cost', 'Buddy Distance', 'Mega Energy Reward',
            'Level', 'CP Multiplier', 'stardust cost', 'sd', 'xl','despawn','Image URL'
        ])
        #* Rearrange the Columns
        self.dfMapData = self.ReArrangeCols(self.dfMapData, ['cp','level','IV','Name','Pokemon Image','Primary Type', 'Secondary Type','Image','MAX CP (IV)','shiny','Remaining Time','Google Maps','Collection Status','Google Maps Link','lat','lng'])
        #* Sort by CP   
        self.dfMapData = self.dfMapData.sort_values(by='cp', ascending=False) 
        #* Convert to JSON Object
        self.jsonMapData = json.loads(self.dfMapData.to_json(orient='records'))
        return self.jsonMapData


class parseRaidsData:

    def __init__(self, maplocation="nyc"):
        self.maplocation = maplocation

    def fetchDataURL(self,url):
        try:
            headers = {'Referer': f'{self.maplocation}/'}
            response = requests.get(url, headers=headers)
            # Check if the response returned a successful status code
            if response.status_code != 200:
                raise Exception(f"Failed to get data, status code: {response.status_code}")
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
            return None
        return response.json()

    def fetchRaidsData(self):
        current_time_seconds = time.time()
        current_time_milliseconds = int(current_time_seconds * 1000)
        self.jsonRaids = self.fetchDataURL(f"{self.maplocation}/raids.php?time={current_time_milliseconds}")
        return self.jsonRaids
    
    def fetchPokemonMoves(self):
        url = f"{self.maplocation}/json/moves.json?ver777" 
        self.dfRaidsMoves = pd.DataFrame(list(self.fetchDataURL(url).items()), columns=['move_id', 'move_name'])
        return self.dfRaidsMoves
    
    
    def ParseRaidsWeatherMovesData(self):
        #* Remove Gyms which dont have much info
        self.dfRaids = pd.DataFrame(self.jsonRaids.get('raids', [])).query("cp != -1").loc[lambda df: df['gym_name'] != '']
        
        #* Add Weather Data
        self.dfWeather = pd.DataFrame(self.jsonRaids.get('weathers', [])).drop_duplicates(subset='cell_id', keep='first')
        self.dfRaids = pd.merge(self.dfRaids, self.dfWeather[['cell_id', 'weather']], on='cell_id', how='left')
        
        #* Add Pokemon Moves
        self.dfRaids[['move1', 'move2']] = self.dfRaids[['move1', 'move2']].astype(str)
        self.dfRaids = self.dfRaids.merge(self.dfRaidsMoves, left_on='move1', right_on='move_id', how='left') \
                                .drop('move_id', axis=1) \
                                .rename(columns={'move_name': 'Move 1 Name'}) \
                                .merge(self.dfRaidsMoves, left_on='move2', right_on='move_id', how='left', suffixes=('', ' 2')) \
                                .drop('move_id', axis=1) \
                                .rename(columns={'move_name': 'Move 2 Name'})
        
        return self.dfRaids

    def ReArrangeCols(self,df, new_column_order):
        valid_columns = [col for col in new_column_order if col in df.columns]
        return df[valid_columns]

    def DropColumns(self,df, columns_to_drop):
        return df.drop(columns=columns_to_drop, errors='ignore').reset_index(drop=True)

    def UpdateTimeStamps(self):
        #* Define the timezone
        tz = pytz.timezone('Asia/Kolkata')
        #* Convert Unix Timestamp to 'HH:MM:SS AM/PM' for each specified column
        for column in ['raid_spawn', 'raid_start', 'raid_end']:
            self.dfRaids[column] = pd.to_datetime(self.dfRaids[column], unit='s')
            self.dfRaids[column] = self.dfRaids[column].dt.tz_localize('UTC').dt.tz_convert(tz)
            self.dfRaids[column] = self.dfRaids[column].dt.strftime('%I:%M:%S %p')
        return self.dfRaids


    def UpdateSpawnTimings(self):
        tz = pytz.timezone('Asia/Kolkata')
        now = datetime.now(tz)
        current_time = datetime.strptime(now.strftime("%I:%M:%S %p"), "%I:%M:%S %p").replace(tzinfo=tz)
        raid_end_time = pd.to_datetime(self.dfRaids['raid_end'], format="%I:%M:%S %p").dt.tz_localize(tz)
        raid_start_time = pd.to_datetime(self.dfRaids['raid_start'], format="%I:%M:%S %p").dt.tz_localize(tz)
        
        self.dfRaids['remaining_time'] = (raid_end_time - current_time).dt.total_seconds().astype(int)
        self.dfRaids['remaining_time_formatted'] = [
            'Expired' if rt <= 0 else 
            'Yet to Start' if rs > current_time else 
            f'{int(rt) // 60:02d}:{int(rt) % 60:02d}'  # Ensure rt is integer for calculations
            for rt, rs in zip(self.dfRaids['remaining_time'], raid_start_time)
        ]

        return self.dfRaids[['raid_spawn', 'raid_start', 'raid_end', 'remaining_time_formatted']]


    def updatePokemonName(self):
        df = pd.read_excel('app/internal/Data/Pokemon Stats.xlsx').drop_duplicates('National Dex')
        self.dfRaids = self.dfRaids.merge(df[['National Dex', 'Name','Types','Weather Boost']], left_on='pokemon_id', right_on='National Dex', how='left').drop(columns='National Dex')
        return self.dfRaids

    def getGoogleMapLinks(self):
        self.dfRaids['Google Maps Link'] = self.dfRaids.apply(lambda row: f"https://www.google.com/maps/?q={row['lat']},{row['lng']}", axis=1)
        return self.dfRaids

    def UpdatePokemonImages(self):
        self.dfRaids['Pokemon Image'] = self.dfRaids.apply(lambda row: f"https://raw.githubusercontent.com/PratikVasagadekar/PokemonGoAssets/main/Images/{row['Name']}.png", axis=1)
        self.dfRaids['Pokemon Team'] = self.dfRaids.apply(lambda row: f"https://raw.githubusercontent.com/PratikVasagadekar/PokemonGoAssets/main/Teams/{row['team']}.png", axis=1)
        self.dfRaids['Primary Type'] = self.dfRaids.apply(lambda row: f"https://raw.githubusercontent.com/PratikVasagadekar/PokemonGoAssets/main/Types/{row['Primary Type']}.png", axis=1)
        return self.dfRaids

    def splitTypesColumn(self):
        self.dfRaids[['Primary Type', 'Secondary Type']] = self.dfRaids['Types'].str.split(', ', expand=True)
        self.dfRaids.drop('Types', axis=1, inplace=True)
        return self.dfRaids

    def UpdateWeatherSettings(self):
        #* Add Weather References
        weather_conditions = {7: "Fog", 6: "Snow", 5: "Windy", 4: "Cloudy", 3: "Partly Cloudy", 2: "Rainy", 1: "Clear"}
        self.dfRaids['weather'] = self.dfRaids['weather'].map(weather_conditions).fillna('')
        #* Add Boosted Condition
        self.dfRaids['Boosted'] = self.dfRaids.apply(
    lambda row: "Boosted" if any(val.strip() in row['weather'] for val in row['Weather Boost'].split(',')) and row['weather'] != "" else "Regular",
    axis=1)

        return self.dfRaids
          
    def UpdateRaidLevelSettings(self):
        #* Level 2 and 4 were Removed in 2020
        level_types = {1: "Level 1", 3: "Level 3", 5: "Level 5", 11: "Level 1 (Shadow)", 13: "Level 3 (Shadow)", 15: "Level 5 (Shadow)", 6: "Mega", 9: "Elite"}
        self.dfRaids['level'] = self.dfRaids['level'].map(level_types)
        return self.dfRaids      
                
    def PokeGoRaidsMap(self):
        try:
            #* The Raids happen at the Day Time only. Hence at the Night Time, the Response would be None       
            #* Lets Create an Empty DF
            self.dfRaids = pd.DataFrame(columns=['Name', 'Pokemon Image', 'Primary Type', 'gym_name', 'lat', 'lng', 'Weather Boost', 'raid_spawn', 'raid_start', 'raid_end', 'remaining_time_formatted', 'pokemon_id', 'level', 'cp', 'Pokemon Team', 'weather', 'Move 1 Name', 'Move 2 Name', 'Google Maps Link'])
             
            #* Fetch Raids Data
            self.fetchRaidsData()

            #* Lets check if the Return is None
            if self.jsonRaids.get("raids", []):
                #* Fetch Pokemon Moves
                self.fetchPokemonMoves()
                #* Parse and Merge Raids, Weather and Moves Data
                self.ParseRaidsWeatherMovesData()

                #* The reason this would happen, is if you check that at start time of eggs.
                if not self.dfRaids.empty:
                    #* Update Spawn Timings
                    self.UpdateTimeStamps()
                    self.UpdateSpawnTimings()
                    #* Update Pokemon ID
                    self.updatePokemonName()
                    #* Update Google Maps Links
                    self.dfRaids = self.getGoogleMapLinks()
                    #* Replace Team Numbers with Names
                    self.dfRaids['team'] = self.dfRaids['team'].replace({0: 'NoTeam', 1: 'Mystic', 2: 'Valor', 3: 'Instinct'}).fillna('Undefined')
                    #* Split Types Column
                    self.dfRaids = self.splitTypesColumn()
                    #* Update Pokemon Images
                    self.dfRaids = self.UpdatePokemonImages()
                    #* Update Weather Conditions and Boosted Status
                    self.dfRaids = self.UpdateWeatherSettings()
                    #* Update Raid Level Settings
                    self.dfRaids = self.UpdateRaidLevelSettings()

                    #* Drop Unwanted Columns
                    self.dfRaids = self.DropColumns(self.dfRaids,['cell_id','ex_raid_eligible','sponsor','move1','move2'])
                    #* Replace Gender with Names
                    self.dfRaids['gender'] = self.dfRaids['gender'].replace({1: 'Male', 2: 'Female', 3: 'Genderless'}).fillna('Undefined')
                    #* Rearrange the Columns
                    self.dfRaids = self.dfRaids[['Name','Pokemon Image','Primary Type','gym_name', 'lat', 'lng','Weather Boost', 'raid_spawn', 'raid_start', 'raid_end', 'remaining_time_formatted','pokemon_id', 'level', 'cp' ,'Pokemon Team', 'weather','Boosted', 'Move 1 Name', 'Move 2 Name','Google Maps Link']]
                    #* Sort by CP   
                    self.dfRaids = self.dfRaids.sort_values(by='cp', ascending=False) 
                    self.dfRaids = self.dfRaids.reset_index(drop=True)
                
            #* Convert to JSON Object
            self.jsonRaidsData = json.loads(self.dfRaids.to_json(orient='records'))

            self.dfRaids.to_csv('./123.csv')
            
            return self.jsonRaidsData
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
