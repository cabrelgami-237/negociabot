from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base
import uuid

class Commande(Base):
    __tablename__ = "commandes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    commercant_id = Column(String, ForeignKey("commercants.id"), nullable=False)
    produit_id = Column(String, ForeignKey("produits.id"), nullable=False)
    client_nom = Column(String, nullable=False)
    client_telephone = Column(String, nullable=False)
    client_quartier = Column(String, nullable=True)
    client_ville = Column(String, nullable=True)
    type_recuperation = Column(String, default="LIVRAISON")
    prix_negocie = Column(Float, nullable=False)
    frais_livraison = Column(Float, default=0)
    prix_total = Column(Float, nullable=False)
    statut = Column(String, default="EN_ATTENTE")
    numero_facture = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
