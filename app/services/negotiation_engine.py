import os
import re
from sqlalchemy.orm import Session
from app.models.produit import Produit
from app.models.conversation import Conversation, Message
from app.models.commercant import Commercant

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def get_openai_client():
    if not OPENAI_API_KEY:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        return None


def extraire_prix(texte):
    nombres = re.findall(r"\d+", texte)
    for n in nombres:
        try:
            val = float(n)
            if val > 100:
                return val
        except:
            pass
    return None


def decider_strategie(prix_propose, produit, nb_tours):
    if prix_propose < produit.prix_plancher:
        return "REFUSER"
    elif prix_propose >= produit.prix_cible:
        return "ACCEPTER"
    elif nb_tours >= 4:
        return "DERNIERE_OFFRE"
    else:
        return "NEGOCIER"


def generer_reponse_bot(message_client, produit, commercant, historique, strategie, prix_propose):
    openai_client = get_openai_client()
    if not openai_client:
        if strategie == "ACCEPTER":
            return "Marche conclu ! " + produit.nom + " a " + str(int(prix_propose)) + " FCFA. Envoyez votre adresse."
        elif strategie == "REFUSER":
            return "Desole, prix minimum " + str(int(produit.prix_plancher)) + " FCFA pour " + produit.nom + "."
        elif strategie == "DERNIERE_OFFRE":
            return "Derniere offre : " + produit.nom + " a " + str(int(produit.prix_cible)) + " FCFA !"
        else:
            contre = int((produit.prix_affiche + produit.prix_cible) / 2)
            return produit.nom + " a " + str(contre) + " FCFA. On s entend ?"
    contre = int((produit.prix_affiche + produit.prix_cible) / 2)
    return produit.nom + " disponible a " + str(contre) + " FCFA."


def traiter_message(commercant_id, produit_id, client_telephone, client_nom, message, db):
    produit = db.query(Produit).filter(Produit.id == produit_id).first()
    if not produit:
        return {"erreur": "Produit introuvable"}
    commercant = db.query(Commercant).filter(Commercant.id == commercant_id).first()
    conversation = db.query(Conversation).filter(
        Conversation.produit_id == produit_id,
        Conversation.client_telephone == client_telephone,
        Conversation.statut == "EN_COURS"
    ).first()
    if not conversation:
        conversation = Conversation(
            commercant_id=commercant_id,
            produit_id=produit_id,
            client_telephone=client_telephone,
            client_nom=client_nom,
            statut="EN_COURS"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    msg_client = Message(conversation_id=conversation.id, expediteur="CLIENT", contenu=message)
    db.add(msg_client)
    historique = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()
    nb_tours = len([m for m in historique if m.expediteur == "CLIENT"])
    prix_propose = extraire_prix(message)
    strategie = decider_strategie(prix_propose, produit, nb_tours) if prix_propose else "NEGOCIER"
    reponse = generer_reponse_bot(message, produit, commercant, historique, strategie, prix_propose)
    msg_bot = Message(conversation_id=conversation.id, expediteur="BOT", contenu=reponse, prix_propose=prix_propose)
    db.add(msg_bot)
    if strategie == "ACCEPTER":
        conversation.statut = "ACCEPTE"
        conversation.prix_final = prix_propose
    elif strategie == "REFUSER" and nb_tours >= 3:
        conversation.statut = "REFUSE"
    db.commit()
    return {
        "conversation_id": conversation.id,
        "reponse_bot": reponse,
        "prix_propose": prix_propose,
        "statut": conversation.statut,
        "prix_final": conversation.prix_final
    }
