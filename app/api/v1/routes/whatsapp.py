from fastapi import APIRouter, Request, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.whatsapp_service import (
    envoyer_message_whatsapp,
    parser_message_entrant,
    WHATSAPP_VERIFY_TOKEN
)
from app.services.negotiation_engine import traiter_message
from app.models.produit import Produit

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp Business"])


@router.get("/webhook")
def verifier_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """Vérification du webhook par Meta"""
    if hub_mode == "subscribe" and hub_verify_token == WHATSAPP_VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Token de verification invalide")


@router.post("/webhook")
async def recevoir_message(request: Request, db: Session = Depends(get_db)):
    """Recevoir et traiter les messages WhatsApp entrants"""
    payload = await request.json()

    # Parser le message entrant
    msg = parser_message_entrant(payload)
    if not msg or not msg["contenu"]:
        return {"statut": "ignored"}

    telephone = msg["telephone"]
    nom = msg["nom"]
    contenu = msg["contenu"]

    # Chercher le produit actif correspondant
    # Par défaut on prend le premier produit disponible
    # Dans une vraie app, le client choisit via un menu
    produit = db.query(Produit).filter(Produit.actif == True).first()
    if not produit:
        envoyer_message_whatsapp(
            telephone,
            "Bonjour ! Aucun produit disponible pour le moment. Revenez bientot !"
        )
        return {"statut": "no_product"}

    # Traiter avec le moteur de négociation
    resultat = traiter_message(
        commercant_id=produit.commercant_id,
        produit_id=produit.id,
        client_telephone=telephone,
        client_nom=nom,
        message=contenu,
        db=db
    )

    # Envoyer la réponse du bot via WhatsApp
    if "reponse_bot" in resultat:
        envoyer_message_whatsapp(telephone, resultat["reponse_bot"])

        # Si accord conclu, envoyer message de confirmation
        if resultat.get("statut") == "ACCEPTE":
            confirmation = (
                "Super ! Marche conclu. "
                "Notre equipe vous contactera sous 24h pour la livraison. "
                "Merci de faire confiance a NegociaBot !"
            )
            envoyer_message_whatsapp(telephone, confirmation)

    return {"statut": "ok", "resultat": resultat}


@router.post("/envoyer")
def envoyer_test(telephone: str, message: str):
    """Endpoint de test pour envoyer un message WhatsApp"""
    resultat = envoyer_message_whatsapp(telephone, message)
    return resultat


@router.get("/config")
def configuration():
    """Voir la configuration WhatsApp actuelle"""
    from app.services.whatsapp_service import WHATSAPP_TOKEN, WHATSAPP_PHONE_ID
    return {
        "webhook_url": "http://votre-domaine.com/whatsapp/webhook",
        "verify_token": WHATSAPP_VERIFY_TOKEN,
        "token_configure": bool(WHATSAPP_TOKEN),
        "phone_id_configure": bool(WHATSAPP_PHONE_ID),
        "mode": "SIMULATION" if not WHATSAPP_TOKEN else "PRODUCTION",
        "instructions": {
            "etape_1": "Creer une app sur developers.facebook.com",
            "etape_2": "Activer WhatsApp Business API",
            "etape_3": "Ajouter WHATSAPP_TOKEN et WHATSAPP_PHONE_ID dans .env",
            "etape_4": "Configurer le webhook avec l'URL ci-dessus",
            "etape_5": "Utiliser verify_token ci-dessus pour la verification"
        }
    }