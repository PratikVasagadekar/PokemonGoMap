# app/routers/pokemon.py

from fastapi import APIRouter,HTTPException, Request
from ..internal.parser import ProcessPokemonGoMapData  # Importing the function from the utilities module

router = APIRouter()

@router.get("/pogomap")
async def process_map_location(request: Request):
    maplocation = request.query_params.get("maplocation")
    if not maplocation:
        raise HTTPException(status_code=422, detail="Map Location is Required")
    
    result = ProcessPokemonGoMapData(maplocation)
    return result