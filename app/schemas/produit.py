from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class ProduitCreate(BaseModel):
    nom: str
    description: Optional[str] = None
    categorie: Optional[str] = None
    prix_affiche: float
    prix_cible: float
    prix_plancher: float
    devise: Optional[str] = "FCFA"

    @validator("prix_plancher")
    def plancher_inferieur_cible(cls, v, values):
        if "prix_cible" in values and v > values["prix_cible"]:
            raise ValueError("Le prix plancher ne peut pas dépasser le prix cible")
        return v

    @validator("prix_cible")
    def cible_inferieur_affiche(cls, v, values):
        if "prix_affiche" in values and v > values["prix_affiche"]:
            raise ValueError("Le prix cible ne peut pas dépasser le prix affiché")
        return v


class ProduitResponse(BaseModel):
    id: str
    commercant_id: str
    nom: str
    description: Optional[str] = None
    categorie: Optional[str] = None
    prix_affiche: float
    prix_cible: float
    prix_plancher: float
    devise: str
    stock_disponible: bool
    actif: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProduitUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    categorie: Optional[str] = None
    prix_affiche: Optional[float] = None
    prix_cible: Optional[float] = None
    prix_plancher: Optional[float] = None
    stock_disponible: Optional[bool] = None
    actif: Optional[bool] = None