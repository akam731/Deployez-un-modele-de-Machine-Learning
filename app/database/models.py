from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Simplification de la classe de base dont tous les models vont hériter
Base = declarative_base()


class Datas(Base):
    """Class représentant la table contenant le dataset du model"""
    __tablename__ = 'datas'     # Nom de la table

    # Colonnes
    id = Column(Integer, primary_key=True, index=True)

class Inputs(Base):
    """Class représentant la table des données entrantes dans l'api"""
    __tablename__ = 'inputs'    # Nom de la table

    # Colonnes
    id = Column(Integer, primary_key=True, index=True)

class Outputs(Base):
    """Class représentant la table des données sortantes de l'api"""
    __tablename__ = 'outputs'   # Nom de la table

    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    input = relationship("Inputs", back_populates="output")             # Relation avec la table input pour relier un input à son/ses outputs
