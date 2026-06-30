from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CommercantCreate(BaseModel):
    nom_boutique: str
    email: EmailStr
    telephone: str
    mot_de_passe: str
    domaine_activite: Optional[str] = None


class CommercantResponse(BaseModel):
    id: str
    nom_boutique: str
    email: str
    telephone: str
    domaine_activite: Optional[str] = None
    plan_abonnement: str
    abonnement_actif: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CommercantLogin(BaseModel):
    email: EmailStr
    mot_de_passe: str