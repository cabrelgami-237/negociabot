from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database.database import Base
import uuid


class Commercant(Base):
    __tablename__ = "commercants"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nom_boutique = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    telephone = Column(String, nullable=False)
    mot_de_passe_hash = Column(String, nullable=False)
    domaine_activite = Column(String, nullable=True)
    plan_abonnement = Column(String, default="GRATUIT")
    abonnement_actif = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())