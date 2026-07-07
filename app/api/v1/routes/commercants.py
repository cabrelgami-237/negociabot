from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.commercant import Commercant
from app.schemas.commercant import CommercantCreate, CommercantResponse
from app.core.security import hacher_mot_de_passe

router = APIRouter(prefix="/commercants", tags=["Commerçants"])


@router.post("/register", response_model=CommercantResponse, status_code=201)
def inscrire_commercant(data: CommercantCreate, db: Session = Depends(get_db)):
    # Vérifier si l'email existe déjà
    existant = db.query(Commercant).filter(
        Commercant.email == data.email
    ).first()
    if existant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un compte avec cet email existe déjà"
        )

    # Créer le nouveau commerçant avec période d'essai gratuite
    nouveau = Commercant(
        nom_boutique=data.nom_boutique,
        email=data.email,
        telephone=data.telephone,
        mot_de_passe_hash=hacher_mot_de_passe(data.mot_de_passe),
        domaine_activite=data.domaine_activite,
        plan_abonnement="GRATUIT",
        abonnement_actif=True
    )

    db.add(nouveau)
    db.commit()
    db.refresh(nouveau)
    return nouveau


@router.get("/{commercant_id}", response_model=CommercantResponse)
def obtenir_commercant(commercant_id: str, db: Session = Depends(get_db)):
    commercant = db.query(Commercant).filter(
        Commercant.id == commercant_id
    ).first()
    if not commercant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commerçant introuvable"
        )
    return commercant
    