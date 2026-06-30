from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AbonnementCreate(BaseModel):
    plan: str  # STARTER ou BUSINESS
    reference_paiement: Optional[str] = None


class AbonnementResponse(BaseModel):
    id: str
    commercant_id: str
    plan: str
    actif: bool
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    montant_paye: Optional[str] = None
    reference_paiement: Optional[str] = None

    class Config:
        from_attributes = True


class PlanInfo(BaseModel):
    nom: str
    prix: str
    description: str
    fonctionnalites: list