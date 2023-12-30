# app/routers/pokemon.py

from fastapi import APIRouter,HTTPException, Request
from ..internal.parser import ProcessPokeGoRaidsData  # Importing the function from the utilities module

router = APIRouter()

@router.get("/pogoraids")
async def process_raids(request: Request):
    maplocation = request.query_params.get("maplocation")
    if not maplocation:
        raise HTTPException(status_code=422, detail="Map Location is Required")
    
    result = ProcessPokeGoRaidsData(maplocation)
    return result