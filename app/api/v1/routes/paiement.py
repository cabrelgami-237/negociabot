from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.database import get_db
from app.models.commercant import Commercant
from app.models.abonnement import Abonnement
from app.services.momo_service import initier_paiement, verifier_paiement
from app.services.orange_money_service import (
    initier_paiement_orange,
    verifier_paiement_orange
)
from datetime import datetime, timedelta

router = APIRouter(prefix="/paiement", tags=["Paiement MTN MoMo & Orange Money"])

PLANS_PRIX = {
    "GRATUIT": 0,
    "STARTER": 5000,
    "BUSINESS": 15000
}


class PaiementRequest(BaseModel):
    commercant_id: str
    telephone: str
    plan: str


class VerificationRequest(BaseModel):
    reference: str
    commercant_id: str
    plan: str


def activer_abonnement(commercant_id: str, plan: str, reference: str, db: Session):
    """Fonction commune pour activer un abonnement après paiement"""
    commercant = db.query(Commercant).filter(
        Commercant.id == commercant_id
    ).first()
    if not commercant:
        return None

    # Désactiver ancien abonnement
    db.query(Abonnement).filter(
        Abonnement.commercant_id == commercant_id,
        Abonnement.actif == True
    ).update({"actif": False})

    # Créer nouvel abonnement
    nouvel_abonnement = Abonnement(
        commercant_id=commercant_id,
        plan=plan,
        actif=True,
        date_debut=datetime.utcnow(),
        date_fin=datetime.utcnow() + timedelta(days=30),
        montant_paye=str(PLANS_PRIX.get(plan, 0)),
        reference_paiement=reference
    )
    db.add(nouvel_abonnement)
    commercant.plan_abonnement = plan
    commercant.abonnement_actif = True
    db.commit()
    return nouvel_abonnement


# ─── MTN MOMO ────────────────────────────────────────────

@router.post("/momo/initier")
def initier_momo(data: PaiementRequest, db: Session = Depends(get_db)):
    commercant = db.query(Commercant).filter(
        Commercant.id == data.commercant_id
    ).first()
    if not commercant:
        raise HTTPException(status_code=404, detail="Commerçant introuvable")
    if data.plan not in PLANS_PRIX:
        raise HTTPException(status_code=400, detail="Plan invalide")

    montant = PLANS_PRIX[data.plan]
    if montant == 0:
        activer_abonnement(data.commercant_id, "GRATUIT", "GRATUIT", db)
        return {"succes": True, "statut": "ACTIVE", "message": "Plan gratuit activé", "plan": "GRATUIT"}

    return initier_paiement(data.telephone, montant, data.plan)


@router.post("/momo/confirmer")
def confirmer_momo(data: VerificationRequest, db: Session = Depends(get_db)):
    statut = verifier_paiement(data.reference)
    if statut["statut"] in ["SUCCESSFUL", "SIMULATION"]:
        abonnement = activer_abonnement(data.commercant_id, data.plan, data.reference, db)
        if not abonnement:
            raise HTTPException(status_code=404, detail="Commerçant introuvable")
        return {
            "succes": True,
            "statut": "ACTIVE",
            "message": f"Abonnement {data.plan} activé via MTN MoMo !",
            "plan": data.plan,
            "date_fin": abonnement.date_fin
        }
    return {"succes": False, "statut": statut["statut"], "message": statut["message"]}


# ─── ORANGE MONEY ────────────────────────────────────────

@router.post("/orange/initier")
def initier_orange(data: PaiementRequest, db: Session = Depends(get_db)):
    commercant = db.query(Commercant).filter(
        Commercant.id == data.commercant_id
    ).first()
    if not commercant:
        raise HTTPException(status_code=404, detail="Commerçant introuvable")
    if data.plan not in PLANS_PRIX:
        raise HTTPException(status_code=400, detail="Plan invalide")

    montant = PLANS_PRIX[data.plan]
    if montant == 0:
        activer_abonnement(data.commercant_id, "GRATUIT", "GRATUIT", db)
        return {"succes": True, "statut": "ACTIVE", "message": "Plan gratuit activé", "plan": "GRATUIT"}

    return initier_paiement_orange(data.telephone, montant, data.plan, data.commercant_id)


@router.post("/orange/confirmer")
def confirmer_orange(data: VerificationRequest, db: Session = Depends(get_db)):
    statut = verifier_paiement_orange(data.reference)
    if statut["statut"] in ["SUCCESSFUL", "SIMULATION"]:
        abonnement = activer_abonnement(data.commercant_id, data.plan, data.reference, db)
        if not abonnement:
            raise HTTPException(status_code=404, detail="Commerçant introuvable")
        return {
            "succes": True,
            "statut": "ACTIVE",
            "message": f"Abonnement {data.plan} activé via Orange Money !",
            "plan": data.plan,
            "date_fin": abonnement.date_fin
        }
    return {"succes": False, "statut": statut["statut"], "message": statut["message"]}


@router.post("/orange/callback")
async def callback_orange(request: Request, db: Session = Depends(get_db)):
    """Webhook Orange Money — notification automatique après paiement"""
    payload = await request.json()
    order_id = payload.get("order_id", "")
    statut = payload.get("status", "")
    if statut == "SUCCESS" and order_id:
        parts = order_id.split("-")
        if len(parts) >= 3:
            plan = parts[-1]
            return {"message": "Callback reçu", "order_id": order_id, "statut": statut}
    return {"message": "Callback reçu", "statut": "ignored"}


# ─── COMPARAISON ─────────────────────────────────────────

@router.get("/methodes")
def methodes_paiement():
    return {
        "methodes": [
            {
                "id": "mtn_momo",
                "nom": "MTN Mobile Money",
                "logo": "MTN",
                "description": "Paiez avec votre compte MTN MoMo",
                "prefixes": ["650", "651", "652", "653", "654", "670", "671", "672", "673", "674", "675", "676", "677", "678", "679"],
                "disponible": True
            },
            {
                "id": "orange_money",
                "nom": "Orange Money",
                "logo": "ORANGE",
                "description": "Paiez avec votre compte Orange Money",
                "prefixes": ["655", "656", "657", "658", "659", "690", "691", "692", "693", "694", "695", "696", "697", "698", "699"],
                "disponible": True
            }
        ],
        "devise": "FCFA",
        "pays": "Cameroun"
    }