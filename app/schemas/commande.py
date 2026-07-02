from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommandeCreate(BaseModel):
    conversation_id: str
    commercant_id: str
    produit_id: str
    client_nom: str
    client_telephone: str
    client_quartier: Optional[str] = None
    client_ville: Optional[str] = None
    type_recuperation: str
    prix_negocie: float

class CommandeResponse(BaseModel):
    id: str
    conversation_id: str
    commercant_id: str
    produit_id: str
    client_nom: str
    client_telephone: str
    client_quartier: Optional[str] = None
    client_ville: Optional[str] = None
    type_recuperation: str
    prix_negocie: float
    frais_livraison: float
    prix_total: float
    statut: str
    numero_facture: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
