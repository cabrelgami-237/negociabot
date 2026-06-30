import uuid
import requests
import os
from datetime import datetime


# Configuration MTN MoMo Sandbox
MOMO_SUBSCRIPTION_KEY = os.getenv("MOMO_SUBSCRIPTION_KEY", "test-subscription-key")
MOMO_API_USER = os.getenv("MOMO_API_USER", "")
MOMO_API_KEY = os.getenv("MOMO_API_KEY", "")
MOMO_BASE_URL = "https://sandbox.momodeveloper.mtn.com"
MOMO_ENVIRONMENT = "sandbox"


def generer_reference():
    return str(uuid.uuid4())


def creer_api_user():
    """Créer un utilisateur API MTN MoMo (sandbox uniquement)"""
    api_user_id = str(uuid.uuid4())
    headers = {
        "X-Reference-Id": api_user_id,
        "Ocp-Apim-Subscription-Key": MOMO_SUBSCRIPTION_KEY,
        "Content-Type": "application/json"
    }
    body = {"providerCallbackHost": "http://localhost:8000"}
    try:
        r = requests.post(
            f"{MOMO_BASE_URL}/v1_0/apiuser",
            json=body,
            headers=headers
        )
        return api_user_id if r.status_code == 201 else None
    except Exception:
        return None


def obtenir_token_acces():
    """Obtenir un token Bearer MTN MoMo"""
    if not MOMO_API_USER or not MOMO_API_KEY:
        return None
    try:
        import base64
        credentials = base64.b64encode(
            f"{MOMO_API_USER}:{MOMO_API_KEY}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {credentials}",
            "Ocp-Apim-Subscription-Key": MOMO_SUBSCRIPTION_KEY,
        }
        r = requests.post(
            f"{MOMO_BASE_URL}/collection/token/",
            headers=headers
        )
        if r.status_code == 200:
            return r.json().get("access_token")
        return None
    except Exception:
        return None


def initier_paiement(telephone: str, montant: float, plan: str) -> dict:
    """
    Initier un paiement MTN MoMo.
    En mode sandbox : simule le paiement si pas de clés configurées.
    """
    reference = generer_reference()

    # Mode simulation (sans clés MoMo réelles)
    if not MOMO_API_USER or not MOMO_API_KEY:
        return {
            "succes": True,
            "reference": reference,
            "statut": "SIMULATION",
            "message": f"Paiement simulé de {montant:.0f} FCFA pour le plan {plan}",
            "telephone": telephone,
            "montant": montant,
            "devise": "XAF",
            "timestamp": datetime.utcnow().isoformat(),
            "mode": "SANDBOX_SIMULATION"
        }

    # Mode réel avec API MTN MoMo
    token = obtenir_token_acces()
    if not token:
        return {
            "succes": False,
            "reference": reference,
            "statut": "ERREUR",
            "message": "Impossible d'obtenir le token MTN MoMo"
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Reference-Id": reference,
        "X-Target-Environment": MOMO_ENVIRONMENT,
        "Ocp-Apim-Subscription-Key": MOMO_SUBSCRIPTION_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "amount": str(int(montant)),
        "currency": "XAF",
        "externalId": reference,
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": telephone.replace("+", "").replace(" ", "")
        },
        "payerMessage": f"Abonnement NégociaBot {plan}",
        "payeeNote": f"Paiement plan {plan}"
    }

    try:
        r = requests.post(
            f"{MOMO_BASE_URL}/collection/v1_0/requesttopay",
            json=body,
            headers=headers
        )
        if r.status_code == 202:
            return {
                "succes": True,
                "reference": reference,
                "statut": "EN_ATTENTE",
                "message": "Demande de paiement envoyée. Confirmez sur votre téléphone.",
                "telephone": telephone,
                "montant": montant,
                "devise": "XAF"
            }
        return {
            "succes": False,
            "reference": reference,
            "statut": "ERREUR",
            "message": f"Erreur MTN MoMo : {r.status_code}"
        }
    except Exception as e:
        return {
            "succes": False,
            "reference": reference,
            "statut": "ERREUR",
            "message": str(e)
        }


def verifier_paiement(reference: str) -> dict:
    """Vérifier le statut d'un paiement"""
    token = obtenir_token_acces()
    if not token:
        # Mode simulation
        return {
            "reference": reference,
            "statut": "SUCCESSFUL",
            "message": "Paiement confirmé (simulation)"
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Target-Environment": MOMO_ENVIRONMENT,
        "Ocp-Apim-Subscription-Key": MOMO_SUBSCRIPTION_KEY,
    }

    try:
        r = requests.get(
            f"{MOMO_BASE_URL}/collection/v1_0/requesttopay/{reference}",
            headers=headers
        )
        if r.status_code == 200:
            data = r.json()
            return {
                "reference": reference,
                "statut": data.get("status", "UNKNOWN"),
                "message": data.get("reason", "")
            }
        return {"reference": reference, "statut": "ERREUR", "message": str(r.status_code)}
    except Exception as e:
        return {"reference": reference, "statut": "ERREUR", "message": str(e)}