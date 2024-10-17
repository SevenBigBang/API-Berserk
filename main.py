from fastapi import FastAPI
from routers.characters import characters_routers

app = FastAPI()

app.include_router(characters_routers.characters_router,
                   prefix="/characters",
                   tags=["Characters"])
