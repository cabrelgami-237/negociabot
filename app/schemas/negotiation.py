from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MessageEntrant(BaseModel):
    produit_id: str
    client_telephone: str
    client_nom: Optional[str] = None
    message: str


class MessageSortant(BaseModel):
    conversation_id: str
    reponse_bot: str
    prix_propose: Optional[float] = None
    statut: str
    prix_final: Optional[float] = None


class ConversationResponse(BaseModel):
    id: str
    commercant_id: str
    produit_id: str
    client_telephone: str
    client_nom: Optional[str] = None
    statut: str
    prix_final: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    expediteur: str
    contenu: str
    prix_propose: Optional[float] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True