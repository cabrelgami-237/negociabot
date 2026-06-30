import requests
import os

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "negociabot2026")
WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"


def envoyer_message_whatsapp(telephone: str, message: str) -> dict:
    """Envoyer un message WhatsApp via l'API Meta"""
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        # Mode simulation
        print(f"[WHATSAPP SIMULATION] -> {telephone}: {message}")
        return {
            "succes": True,
            "mode": "SIMULATION",
            "telephone": telephone,
            "message": message
        }

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "messaging_product": "whatsapp",
        "to": telephone.replace("+", "").replace(" ", ""),
        "type": "text",
        "text": {"body": message}
    }

    try:
        r = requests.post(WHATSAPP_API_URL, json=body, headers=headers)
        if r.status_code == 200:
            return {"succes": True, "data": r.json()}
        return {"succes": False, "erreur": r.text}
    except Exception as e:
        return {"succes": False, "erreur": str(e)}


def envoyer_message_template(telephone: str, template: str, langue: str = "fr") -> dict:
    """Envoyer un template WhatsApp approuvé"""
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
        print(f"[WHATSAPP TEMPLATE SIMULATION] -> {telephone}: {template}")
        return {"succes": True, "mode": "SIMULATION"}

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "messaging_product": "whatsapp",
        "to": telephone.replace("+", "").replace(" ", ""),
        "type": "template",
        "template": {
            "name": template,
            "language": {"code": langue}
        }
    }

    try:
        r = requests.post(WHATSAPP_API_URL, json=body, headers=headers)
        return {"succes": r.status_code == 200, "data": r.json()}
    except Exception as e:
        return {"succes": False, "erreur": str(e)}


def parser_message_entrant(payload: dict) -> dict | None:
    """Parser un message WhatsApp entrant depuis le webhook Meta"""
    try:
        entry = payload["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" not in value:
            return None

        message = value["messages"][0]
        contact = value["contacts"][0]

        return {
            "telephone": message["from"],
            "nom": contact["profile"]["name"],
            "message_id": message["id"],
            "type": message["type"],
            "contenu": message["text"]["body"] if message["type"] == "text" else "",
            "timestamp": message["timestamp"]
        }
    except (KeyError, IndexError):
        return None