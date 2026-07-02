code = """import os
import re
from sqlalchemy.orm import Session
from app.models.produit import Produit
from app.models.conversation import Conversation, Message
from app.models.commercant import Commercant
from app.models.commande import Commande
from app.services.livraison_service import calculer_frais_livraison, get_adresse_boutique
from app.services.facture_service import generer_numero_facture, envoyer_facture_client, envoyer_notification_commercant

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

ETAPES = {
    "NEGOCIATION": "negociation",
    "CHOIX_RECUPERATION": "choix_recuperation",
    "COLLECTE_NOM": "collecte_nom",
    "COLLECTE_QUARTIER": "collecte_quartier",
    "COLLECTE_TELEPHONE": "collecte_telephone",
    "CONFIRMATION": "confirmation",
    "TERMINEE": "terminee"
}

def get_openai_client():
    if not OPENAI_API_KEY:
        return None
    try:
        from openai import OpenAI
        return openai_client(api_key=OPENAI_API_KEY)
    except Exception:
        return None

def extraire_prix(texte):
    nombres = re.findall(r"\\d+", texte)
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

def generer_reponse_negociation(message_client, produit, strategie, prix_propose, nb_tours):
    if strategie == "ACCEPTER":
        return ("ACCORD", "Super, marche conclu ! " + produit.nom + " a " + str(int(prix_propose)) + " FCFA. Comment souhaitez-vous recuperer votre commande ?\\n\\n1 - Livraison a domicile\\n2 - Je viens en boutique")
    elif strategie == "REFUSER":
        return ("REFUS", "Desole, je ne peux pas descendre en dessous de " + str(int(produit.prix_plancher)) + " FCFA pour " + produit.nom + ". C est mon prix minimum.")
    elif strategie == "DERNIERE_OFFRE":
        return ("NEGOCIATION", "Derniere offre : " + produit.nom + " a " + str(int(produit.prix_cible)) + " FCFA. C est vraiment mon meilleur prix !")
    else:
        contre = int((produit.prix_affiche + produit.prix_cible) / 2)
        if nb_tours == 0:
            return ("NEGOCIATION", "Bonjour ! Le " + produit.nom + " est a " + str(int(produit.prix_affiche)) + " FCFA. C est de la qualite superieure ! Je peux faire un effort pour vous.")
        else:
            return ("NEGOCIATION", "Hmm " + str(int(prix_propose)) + " FCFA c est un peu juste. Je peux vous faire " + str(contre) + " FCFA, c est mon meilleur effort !")

def get_etape_conversation(conversation_id: str, db: Session) -> str:
    commande = db.query(Commande).filter(
        Commande.conversation_id == conversation_id
    ).first()
    if not commande:
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conv and conv.statut == "ACCEPTE":
            return ETAPES["CHOIX_RECUPERATION"]
        return ETAPES["NEGOCIATION"]
    if commande.statut == "EN_ATTENTE":
        if not commande.type_recuperation or commande.type_recuperation == "":
            return ETAPES["CHOIX_RECUPERATION"]
        if not commande.client_nom or commande.client_nom == "":
            return ETAPES["COLLECTE_NOM"]
        if commande.type_recuperation == "LIVRAISON" and (not commande.client_quartier or commande.client_quartier == ""):
            return ETAPES["COLLECTE_QUARTIER"]
        if not commande.client_telephone or commande.client_telephone == "":
            return ETAPES["COLLECTE_TELEPHONE"]
        return ETAPES["CONFIRMATION"]
    return ETAPES["TERMINEE"]

def traiter_message(commercant_id, produit_id, client_telephone, client_nom, message, db: Session):
    produit = db.query(Produit).filter(Produit.id == produit_id).first()
    if not produit:
        return {"erreur": "Produit introuvable"}
    commercant = db.query(Commercant).filter(Commercant.id == commercant_id).first()

    conversation = db.query(Conversation).filter(
        Conversation.produit_id == produit_id,
        Conversation.client_telephone == client_telephone,
        Conversation.statut.in_(["EN_COURS", "ACCEPTE"])
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

    etape = get_etape_conversation(conversation.id, db)
    message_lower = message.lower().strip()

    # ETAPE : CHOIX RECUPERATION
    if etape == ETAPES["CHOIX_RECUPERATION"]:
        if "1" in message or "livraison" in message_lower or "domicile" in message_lower:
            commande = Commande(
                conversation_id=conversation.id,
                commercant_id=commercant_id,
                produit_id=produit_id,
                client_nom="",
                client_telephone=client_telephone,
                type_recuperation="LIVRAISON",
                prix_negocie=conversation.prix_final or produit.prix_cible,
                frais_livraison=0,
                prix_total=conversation.prix_final or produit.prix_cible
            )
            db.add(commande)
            db.commit()
            reponse = "Super ! Pour la livraison, j ai besoin de quelques infos.\\nVotre nom complet s il vous plait ?"
        elif "2" in message or "boutique" in message_lower or "viens" in message_lower:
            commande = Commande(
                conversation_id=conversation.id,
                commercant_id=commercant_id,
                produit_id=produit_id,
                client_nom="",
                client_telephone=client_telephone,
                type_recuperation="BOUTIQUE",
                prix_negocie=conversation.prix_final or produit.prix_cible,
                frais_livraison=0,
                prix_total=conversation.prix_final or produit.prix_cible
            )
            db.add(commande)
            db.commit()
            boutique = get_adresse_boutique()
            reponse = "Tres bien ! Voici notre adresse :\\n\\nAdresse : " + boutique["adresse"] + "\\nHoraires : " + boutique["horaires"] + "\\nTel : " + boutique["telephone"] + "\\n\\nVotre nom complet s il vous plait ?"
        else:
            reponse = "Veuillez choisir :\\n\\n1 - Livraison a domicile\\n2 - Je viens en boutique"

        msg_bot = Message(conversation_id=conversation.id, expediteur="BOT", contenu=reponse)
        db.add(msg_bot)
        db.commit()
        return {"conversation_id": conversation.id, "reponse_bot": reponse, "prix_propose": None, "statut": conversation.statut, "prix_final": conversation.prix_final}

    # ETAPE : COLLECTE NOM
    if etape == ETAPES["COLLECTE_NOM"]:
        commande = db.query(Commande).filter(Commande.conversation_id == conversation.id).first()
        commande.client_nom = message.strip()
        db.commit()
        if commande.type_recuperation == "LIVRAISON":
            reponse = "Merci " + message.strip() + " ! Votre quartier ou ville de livraison ?"
        else:
            reponse = "Merci " + message.strip() + " ! Votre numero de telephone pour qu on vous contacte ?"
        msg_bot = Message(conversation_id=conversation.id, expediteur="BOT", contenu=reponse)
        db.add(msg_bot)
        db.commit()
        return {"conversation_id": conversation.id, "reponse_bot": reponse, "prix_propose": None, "statut": conversation.statut, "prix_final": conversation.prix_final}

    # ETAPE : COLLECTE QUARTIER
    if etape == ETAPES["COLLECTE_QUARTIER"]:
        commande = db.query(Commande).filter(Commande.conversation_id == conversation.id).first()
        commande.client_quartier = message.strip()
        livraison = calculer_frais_livraison(message.strip())
        commande.frais_livraison = livraison["frais"]
        commande.prix_total = commande.prix_negocie + livraison["frais"]
        db.commit()
        reponse = "Super ! Votre numero de telephone pour le livreur ?"
        msg_bot = Message(conversation_id=conversation.id, expediteur="BOT", contenu=reponse)
        db.add(msg_bot)
        db.commit()
        return {"conversation_id": conversation.id, "reponse_bot": reponse, "prix_propose": None, "statut": conversation.statut, "prix_final": conversation.prix_final}

    # ETAPE : COLLECTE TELEPHONE
    if etape == ETAPES["COLLECTE_TELEPHONE"]:
        commande = db.query(Commande).filter(Commande.conversation_id == conversation.id).first()
        commande.client_telephone = message.strip()
        db.commit()

        if commande.type_recuperation == "LIVRAISON":
            recap = ("Recapitulatif de votre commande :\\n\\n"
                    "Produit : " + produit.nom + "\\n"
                    "Prix negocie : " + str(int(commande.prix_negocie)) + " FCFA\\n"
                    "Livraison " + (commande.client_quartier or "") + " : " + str(int(commande.frais_livraison)) + " FCFA\\n"
                    "──────────────────\\n"
                    "TOTAL : " + str(int(commande.prix_total)) + " FCFA\\n\\n"
                    "Paiement a la livraison\\n\\n"
                    "Confirmez-vous la commande ? Repondez OUI pour valider")
        else:
            recap = ("Recapitulatif de votre commande :\\n\\n"
                    "Produit : " + produit.nom + "\\n"
                    "Prix negocie : " + str(int(commande.prix_negocie)) + " FCFA\\n"
                    "Retrait en boutique : Gratuit\\n"
                    "──────────────────\\n"
                    "TOTAL : " + str(int(commande.prix_total)) + " FCFA\\n\\n"
                    "Paiement a la livraison\\n\\n"
                    "Confirmez-vous la commande ? Repondez OUI pour valider")

        msg_bot = Message(conversation_id=conversation.id, expediteur="BOT", contenu=recap)
        db.add(msg_bot)
        db.commit()
        return {"conversation_id": conversation.id, "reponse_bot": recap, "prix_propose": None, "statut": conversation.statut, "prix_final": conversation.prix_final}

    # ETAPE : CONFIRMATION
    if etape == ETAPES["CONFIRMATION"]:
        commande = db.query(Commande).filter(Commande.conversation_id == conversation.id).first()
        if "oui" in message_lower or "yes" in message_lower or "ok" in message_lower or "confirme" in message_lower:
            numero_facture = generer_numero_facture()
            commande.numero_facture = numero_facture
            commande.statut = "CONFIRMEE"
            conversation.statut = "TERMINEE"
            db.commit()

            commande_data = {
                "numero_facture": numero_facture,
                "client_nom": commande.client_nom,
                "client_telephone": commande.client_telephone,
                "client_quartier": commande.client_quartier or "",
                "produit_nom": produit.nom,
                "prix_negocie": commande.prix_negocie,
                "frais_livraison": commande.frais_livraison,
                "prix_total": commande.prix_total,
                "type_recuperation": commande.type_recuperation,
                "boutique_nom": commercant.nom_boutique if commercant else "NegociaBot"
            }

            envoyer_facture_client(commande.client_telephone, commande_data)
            if commercant:
                envoyer_notification_commercant(client_telephone, commande_data)

            reponse = ("Commande confirmee ! Votre facture N " + numero_facture + " a ete envoyee.\\n\\n"
                      "Notre equipe vous contactera sous 2h pour la livraison.\\n"
                      "Merci " + commande.client_nom + " de faire confiance a " + (commercant.nom_boutique if commercant else "NegociaBot") + " !")
        else:
            reponse = "Commande annulee. N hesitez pas a revenir si vous changez d avis !"
            commande.statut = "ANNULEE"
            db.commit()

        msg_bot = Message(conversation_id=conversation.id, expediteur="BOT", contenu=reponse)
        db.add(msg_bot)
        db.commit()
        return {"conversation_id": conversation.id, "reponse_bot": reponse, "prix_propose": None, "statut": conversation.statut, "prix_final": conversation.prix_final}

    # ETAPE : NEGOCIATION (defaut)
    historique = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()
    nb_tours = len([m for m in historique if m.expediteur == "CLIENT"])
    prix_propose = extraire_prix(message)
    strategie = decider_strategie(prix_propose, produit, nb_tours) if prix_propose else "NEGOCIER"
    resultat, reponse = generer_reponse_negociation(message, produit, strategie, prix_propose, nb_tours)

    msg_bot = Message(conversation_id=conversation.id, expediteur="BOT", contenu=reponse, prix_propose=prix_propose)
    db.add(msg_bot)

    if resultat == "ACCORD":
        conversation.statut = "ACCEPTE"
        conversation.prix_final = prix_propose
    elif resultat == "REFUS" and nb_tours >= 3:
        conversation.statut = "REFUSE"

    db.commit()
    return {"conversation_id": conversation.id, "reponse_bot": reponse, "prix_propose": prix_propose, "statut": conversation.statut, "prix_final": conversation.prix_final}
"""

with open("app/services/negotiation_engine.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Moteur de negociation v2 ecrit avec succes !")