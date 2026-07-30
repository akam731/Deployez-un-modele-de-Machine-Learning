from fastapi import FastAPI

# Création du serveur
app = FastAPI()


@app.get("/",
    summary="Endpoint principal",
    description="Retourne un message de bienvenue.")
async def root():
    return {"message": "Hello World"}