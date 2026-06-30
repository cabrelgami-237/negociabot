from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.abonnement import Abonnement
from app.models.commercant import Commercant
from app.schemas.abonnement import AbonnementCreate, AbonnementResponse, PlanInfo
from datetime import datetime, timedelta

router = APIRouter(prefix="/abonnements", tags=["Abonnements"])

PLANS = {
    "GRATUIT": {
        "nom": "Gratuit",
        "prix": "0 FCFA",
        "description": "Accès limité pour tester NégociaBot",
        "fonctionnalites": ["1 produit", "10 négociations/mois", "Support email"],
        "duree_jours": 30,
        "montant": "0"
    },
    "STARTER": {
        "nom": "Starter",
        "prix": "5 000 FCFA/mois",
        "description": "Pour les petits commerçants",
        "fonctionnalites": ["10 produits", "100 négociations/mois", "WhatsApp bot", "Support prioritaire"],
        "duree_jours": 30,
        "montant": "5000"
    },
    "BUSINESS": {
        "nom": "Business",
        "prix": "15 000 FCFA/mois",
        "description": "Pour les commerçants professionnels",
        "fonctionnalites": ["Produits illimités", "Négociations illimitées", "WhatsApp + Facebook + Instagram", "Tableau de bord analytique", "Support 24/7"],
        "duree_jours": 30,
        "montant": "15000"
    }
}


@router.get("/plans")
def obtenir_plans():
    return PLANS


@router.post("/souscrire/{commercant_id}", response_model=AbonnementResponse)
def souscrire_abonnement(
    commercant_id: str,
    data: AbonnementCreate,
    db: Session = Depends(get_db)
):
    # Vérifier que le commerçant existe
    commercant = db.query(Commercant).filter(
        Commercant.id == commercant_id
    ).first()
    if not commercant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commerçant introuvable"
        )

    # Vérifier que le plan existe
    if data.plan not in PLANS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plan invalide. Choisir parmi : {list(PLANS.keys())}"
        )

    plan_info = PLANS[data.plan]

    # Désactiver l'ancien abonnement
    db.query(Abonnement).filter(
        Abonnement.commercant_id == commercant_id,
        Abonnement.actif == True
    ).update({"actif": False})

    # Créer le nouvel abonnement
    nouvel_abonnement = Abonnement(
        commercant_id=commercant_id,
        plan=data.plan,
        actif=True,
        date_debut=datetime.utcnow(),
        date_fin=datetime.utcnow() + timedelta(days=plan_info["duree_jours"]),
        montant_paye=plan_info["montant"],
        reference_paiement=data.reference_paiement
    )

    db.add(nouvel_abonnement)

    # Mettre à jour le commerçant
    commercant.plan_abonnement = data.plan
    commercant.abonnement_actif = True

    db.commit()
    db.refresh(nouvel_abonnement)
    return nouvel_abonnement