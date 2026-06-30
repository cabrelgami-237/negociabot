from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base
import uuid


class Abonnement(Base):
    __tablename__ = "abonnements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    commercant_id = Column(String, ForeignKey("commercants.id"), nullable=False)
    plan = Column(String, nullable=False)  # GRATUIT, STARTER, BUSINESS
    actif = Column(Boolean, default=True)
    date_debut = Column(DateTime(timezone=True), server_default=func.now())
    date_fin = Column(DateTime(timezone=True), nullable=True)
    montant_paye = Column(String, nullable=True)
    reference_paiement = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())