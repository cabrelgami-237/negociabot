from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.negotiation import MessageEntrant, MessageSortant, ConversationResponse
from app.services.negotiation_engine import traiter_message
from app.models.conversation import Conversation, Message
from app.schemas.negotiation import MessageResponse
from typing import List

router = APIRouter(prefix="/negotiation", tags=["Négociation IA"])


@router.post("/message/{commercant_id}", response_model=MessageSortant)
def envoyer_message(
    commercant_id: str,
    data: MessageEntrant,
    db: Session = Depends(get_db)
):
    resultat = traiter_message(
        commercant_id=commercant_id,
        produit_id=data.produit_id,
        client_telephone=data.client_telephone,
        client_nom=data.client_nom or "Client",
        message=data.message,
        db=db
    )
    if "erreur" in resultat:
        raise HTTPException(status_code=404, detail=resultat["erreur"])
    return resultat


@router.get("/conversations/{commercant_id}", response_model=List[ConversationResponse])
def obtenir_conversations(
    commercant_id: str,
    db: Session = Depends(get_db)
):
    conversations = db.query(Conversation).filter(
        Conversation.commercant_id == commercant_id
    ).order_by(Conversation.created_at.desc()).all()
    return conversations


@router.get("/historique/{conversation_id}", response_model=List[MessageResponse])
def obtenir_historique(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()
    return messages