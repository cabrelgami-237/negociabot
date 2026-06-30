from sqlalchemy import Column, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base
import uuid


class Produit(Base):
    __tablename__ = "produits"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    commercant_id = Column(String, ForeignKey("commercants.id"), nullable=False)
    nom = Column(String, nullable=False)
    description = Column(String, nullable=True)
    categorie = Column(String, nullable=True)
    prix_affiche = Column(Float, nullable=False)
    prix_cible = Column(Float, nullable=False)
    prix_plancher = Column(Float, nullable=False)
    devise = Column(String, default="FCFA")
    stock_disponible = Column(Boolean, default=True)
    actif = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    