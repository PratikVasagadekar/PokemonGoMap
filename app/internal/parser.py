from .utils import parseMapData,parseRaidsData

def ProcessPokemonGoMapData(maplocation='nyc'):
    #* Create the Class Instance
    clsPokemonMapData = parseMapData(maplocation=maplocation)

    #* Process and Load the Map Data
    jsonMapData = clsPokemonMapData.ProcessMapData()

    return jsonMapData

def ProcessPokeGoRaidsData(maplocation='nyc'):
    #* Create the Class Instance
    clsPokemonRaidsData = parseRaidsData(maplocation=maplocation)

    #* Process and Load the Map Data
    jsonRaidsData = clsPokemonRaidsData.PokeGoRaidsMap()

    return jsonRaidsData


