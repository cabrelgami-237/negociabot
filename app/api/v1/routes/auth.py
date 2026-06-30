from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.commercant import Commercant
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import (
    verifier_mot_de_passe,
    creer_token_acces,
    decoder_token
)

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/login", response_model=TokenResponse)
def se_connecter(data: LoginRequest, db: Session = Depends(get_db)):
    # Chercher le commerçant dans la base de données
    commercant = db.query(Commercant).filter(
        Commercant.email == data.email
    ).first()

    if not commercant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"
        )

    if not verifier_mot_de_passe(data.mot_de_passe, commercant.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects"
        )

    if not commercant.abonnement_actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Abonnement expire. Renouvelez pour continuer."
        )

    token = creer_token_acces({
        "sub": commercant.id,
        "email": commercant.email
    })

    return TokenResponse(
        access_token=token,
        commercant_id=commercant.id,
        nom_boutique=commercant.nom_boutique,
        plan_abonnement=commercant.plan_abonnement
    )


@router.get("/me")
def mon_profil(token: str, db: Session = Depends(get_db)):
    payload = decoder_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expire"
        )
    commercant = db.query(Commercant).filter(
        Commercant.id == payload.get("sub")
    ).first()
    if not commercant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commerçant introuvable"
        )
    return {
        "commercant_id": commercant.id,
        "email": commercant.email,
        "nom_boutique": commercant.nom_boutique,
        "plan_abonnement": commercant.plan_abonnement
    }