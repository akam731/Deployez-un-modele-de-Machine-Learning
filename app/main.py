from fastapi import FastAPI

# Création du serveur FastAPI
app = FastAPI(
    title="ESN TechNova Partners - API",
    description="Identifiez les causes d'attrition au sein de l'ESN TechNova Partners",
    version="1.0.0",
)

from app.api import routes  # noqa: F401