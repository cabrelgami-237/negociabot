import requests
import os
import base64
from datetime import datetime
import uuid

# Configuration Orange Money Cameroun
ORANGE_CLIENT_ID = os.getenv("ORANGE_CLIENT_ID", "")
ORANGE_CLIENT_SECRET = os.getenv("ORANGE_CLIENT_SECRET", "")
ORANGE_BASE_URL = "https://api.orange.com"
ORANGE_MERCHANT_KEY = os.getenv("ORANGE_MERCHANT_KEY", "")
ORANGE_NOTIF_URL = os.getenv("ORANGE_NOTIF_URL", "http://localhost:8000/paiement/orange/callback")
ORANGE_RETURN_URL = os.getenv("ORANGE_RETURN_URL", "http://localhost:3000/abonnement/succes")
ORANGE_CANCEL_URL = os.getenv("ORANGE_CANCEL_URL", "http://localhost:3000/abonnement/annule")


def obtenir_token_orange() -> str | None:
    """Obtenir le token d'accès Orange Money"""
    if not ORANGE_CLIENT_ID or not ORANGE_CLIENT_SECRET:
        return None
    try:
        credentials = base64.b64encode(
            f"{ORANGE_CLIENT_ID}:{ORANGE_CLIENT_SECRET}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        r = requests.post(
            f"{ORANGE_BASE_URL}/oauth/v3/token",
            data={"grant_type": "client_credentials"},
            headers=headers
        )
        if r.status_code == 200:
            return r.json().get("access_token")
        return None
    except Exception:
        return None


def initier_paiement_orange(
    telephone: str,
    montant: float,
    plan: str,
    commercant_id: str
) -> dict:
    """
    Initier un paiement Orange Money Cameroun.
    Mode simulation si pas de clés configurées.
    """
    reference = str(uuid.uuid4())[:8].upper()
    order_id = f"NB-{reference}-{plan}"

    # Mode simulation
    if not ORANGE_CLIENT_ID or not ORANGE_CLIENT_SECRET:
        return {
            "succes": True,
            "reference": order_id,
            "statut": "SIMULATION",
            "message": f"Paiement Orange Money simulé de {montant:.0f} FCFA pour le plan {plan}",
            "telephone": telephone,
            "montant": montant,
            "devise": "XAF",
            "timestamp": datetime.utcnow().isoformat(),
            "mode": "SANDBOX_SIMULATION",
            "payment_url": None
        }

    # Mode réel
    token = obtenir_token_orange()
    if not token:
        return {
            "succes": False,
            "reference": order_id,
            "statut": "ERREUR",
            "message": "Impossible d'obtenir le token Orange Money"
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "merchant_key": ORANGE_MERCHANT_KEY,
        "currency": "XAF",
        "order_id": order_id,
        "amount": int(montant),
        "return_url": ORANGE_RETURN_URL,
        "cancel_url": ORANGE_CANCEL_URL,
        "notif_url": ORANGE_NOTIF_URL,
        "lang": "fr",
        "reference": f"NegociaBot {plan} - {telephone}"
    }

    try:
        r = requests.post(
            f"{ORANGE_BASE_URL}/orange-money-webpay/cm/v1/webpayment",
            json=body,
            headers=headers
        )
        if r.status_code == 200:
            data = r.json()
            return {
                "succes": True,
                "reference": order_id,
                "statut": "EN_ATTENTE",
                "message": "Redirection vers Orange Money...",
                "payment_url": data.get("payment_url"),
                "pay_token": data.get("pay_token"),
                "telephone": telephone,
                "montant": montant,
                "devise": "XAF"
            }
        return {
            "succes": False,
            "reference": order_id,
            "statut": "ERREUR",
            "message": f"Erreur Orange Money : {r.status_code} - {r.text}"
        }
    except Exception as e:
        return {
            "succes": False,
            "reference": order_id,
            "statut": "ERREUR",
            "message": str(e)
        }


def verifier_paiement_orange(order_id: str) -> dict:
    """Vérifier le statut d'un paiement Orange Money"""
    if not ORANGE_CLIENT_ID or not ORANGE_CLIENT_SECRET:
        return {
            "order_id": order_id,
            "statut": "SUCCESSFUL",
            "message": "Paiement confirmé (simulation Orange Money)"
        }

    token = obtenir_token_orange()
    if not token:
        return {"order_id": order_id, "statut": "ERREUR", "message": "Token invalide"}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.get(
            f"{ORANGE_BASE_URL}/orange-money-webpay/cm/v1/webpayment/{order_id}",
            headers=headers
        )
        if r.status_code == 200:
            data = r.json()
            return {
                "order_id": order_id,
                "statut": data.get("status", "UNKNOWN"),
                "message": data.get("message", ""),
                "montant": data.get("amount"),
                "telephone": data.get("subscriber_msisdn")
            }
        return {"order_id": order_id, "statut": "ERREUR", "message": str(r.status_code)}
    except Exception as e:
        return {"order_id": order_id, "statut": "ERREUR", "message": str(e)}