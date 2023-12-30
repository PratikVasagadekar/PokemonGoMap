from fastapi import FastAPI
from .routers import pokegomap
from .routers import pokegoraids

app = FastAPI()

app.include_router(pokegomap.router, prefix="/pokemongo")
app.include_router(pokegoraids.router, prefix="/pokemongo")

@app.get("/")
async def show_root():
    return {"Welcome to the Club"}


