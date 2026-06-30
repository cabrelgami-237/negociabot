from sqlalchemy import Column, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.sql import func
from app.database.database import Base
import uuid


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    commercant_id = Column(String, ForeignKey("commercants.id"), nullable=False)
    produit_id = Column(String, ForeignKey("produits.id"), nullable=False)
    client_telephone = Column(String, nullable=False)
    client_nom = Column(String, nullable=True)
    statut = Column(String, default="EN_COURS")  # EN_COURS, ACCEPTE, REFUSE, EXPIRE
    prix_final = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    expediteur = Column(String, nullable=False)  # CLIENT ou BOT
    contenu = Column(Text, nullable=False)
    prix_propose = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())