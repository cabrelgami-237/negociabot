from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.database import get_db
from app.models.conversation import Conversation
from app.models.produit import Produit
from app.models.abonnement import Abonnement

router = APIRouter(prefix="/dashboard", tags=["Tableau de bord"])


@router.get("/{commercant_id}")
def tableau_de_bord(commercant_id: str, db: Session = Depends(get_db)):
    # Statistiques des conversations
    total = db.query(Conversation).filter(
        Conversation.commercant_id == commercant_id
    ).count()

    acceptees = db.query(Conversation).filter(
        Conversation.commercant_id == commercant_id,
        Conversation.statut == "ACCEPTE"
    ).count()

    refusees = db.query(Conversation).filter(
        Conversation.commercant_id == commercant_id,
        Conversation.statut == "REFUSE"
    ).count()

    en_cours = db.query(Conversation).filter(
        Conversation.commercant_id == commercant_id,
        Conversation.statut == "EN_COURS"
    ).count()

    # Chiffre d'affaires
    ca = db.query(func.sum(Conversation.prix_final)).filter(
        Conversation.commercant_id == commercant_id,
        Conversation.statut == "ACCEPTE"
    ).scalar() or 0

    # Produits actifs
    nb_produits = db.query(Produit).filter(
        Produit.commercant_id == commercant_id,
        Produit.actif == True
    ).count()

    # Abonnement actif
    abonnement = db.query(Abonnement).filter(
        Abonnement.commercant_id == commercant_id,
        Abonnement.actif == True
    ).first()

    return {
        "commercant_id": commercant_id,
        "negotiations": {
            "total": total,
            "acceptees": acceptees,
            "refusees": refusees,
            "en_cours": en_cours,
            "taux_succes": round((acceptees / total * 100), 1) if total > 0 else 0
        },
        "chiffre_affaires": {
            "total_fcfa": ca,
            "devise": "FCFA"
        },
        "produits_actifs": nb_produits,
        "abonnement": {
            "plan": abonnement.plan if abonnement else "GRATUIT",
            "actif": abonnement.actif if abonnement else False,
            "date_fin": abonnement.date_fin if abonnement else None
        }
    }