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

ETAPE_NEGOCIATION = "negociation"
ETAPE_CHOIX = "choix_recuperation"
ETAPE_NOM = "collecte_nom"
ETAPE_QUARTIER = "collecte_quartier"
ETAPE_TEL_LIVRAISON = "collecte_tel_livraison"
ETAPE_CONFIRMATION = "confirmation"
ETAPE_TERMINEE = "terminee"


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
        reponse = ("Super, marche conclu ! " + produit.nom + " a " + str(int(prix_propose)) + " FCFA. "
                  "Comment souhaitez-vous recuperer votre commande ?\\n\\n"
                  "1 - Livraison a domicile\\n"
                  "2 - Je viens en boutique")
        return ("ACCORD", reponse)
    elif strategie == "REFUSER":
        return ("REFUS", "Desole, je ne peux pas descendre en dessous de " + str(int(produit.prix_plancher)) + " FCFA. C est mon prix minimum.")
    elif strategie == "DERNIERE_OFFRE":
        return ("NEGOCIATION", "Derniere offre : " + produit.nom + " a " + str(int(produit.prix_cible)) + " FCFA. C est vraiment mon meilleur prix !")
    else:
        contre = int((produit.prix_affiche + produit.prix_cible) / 2)
        if prix_propose is None or nb_tours == 0:
            return ("NEGOCIATION", "Bonjour ! Le " + produit.nom + " est a " + str(int(produit.prix_affiche)) + " FCFA. C est de la qualite superieure ! Je peux faire un effort pour vous.")
        else:
            return ("NEGOCIATION", "Hmm " + str(int(prix_propose)) + " FCFA c est un peu juste. Je peux vous faire " + str(contre) + " FCFA, c est mon meilleur effort !")


def get_etape(conversation_id, db):
    commande = db.query(Commande).filter(Commande.conversation_id == conversation_id).first()
    if not commande:
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conv and conv.statut == "ACCEPTE":
            return ETAPE_CHOIX
        return ETAPE_NEGOCIATION
    if commande.statut in ["CONFIRMEE", "ANNULEE"]:
        return ETAPE_TERMINEE
    if not commande.type_recuperation:
        return ETAPE_CHOIX
    if not commande.client_nom:
        return ETAPE_NOM
    if commande.type_recuperation == "LIVRAISON" and not commande.client_quartier:
        return ETAPE_QUARTIER
    if commande.type_recuperation == "LIVRAISON" and commande.client_quartier and commande.frais_livraison == 0:
        return ETAPE_TEL_LIVRAISON
    return ETAPE_CONFIRMATION


def traiter_message(commercant_id, produit_id, client_telephone, client_nom, message, db):
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
    db.commit()

    etape = get_etape(conversation.id, db)
    message_lower = message.lower().strip()

    def sauver_reponse(reponse):
        msg_bot = Message(conversation_id=conversation.id, expediteur="BOT", contenu=reponse)
        db.add(msg_bot)
        db.commit()
        return {
            "conversation_id": conversation.id,
            "reponse_bot": reponse,
            "prix_propose": None,
            "statut": conversation.statut,
            "prix_final": conversation.prix_final
        }

    if etape == ETAPE_CHOIX:
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
                prix_total=0
            )
            db.add(commande)
            db.commit()
            return sauver_reponse("Super ! Pour la livraison, j ai besoin de quelques infos.\\nVotre nom complet s il vous plait ?")
        elif message.strip() == "2" or "boutique" in message_lower or "viens" in message_lower:
            boutique = get_adresse_boutique()
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
            reponse = ("Tres bien ! Voici notre adresse :\\n\\n"
                      "Adresse : " + boutique["adresse"] + "\\n"
                      "Horaires : " + boutique["horaires"] + "\\n\\n"
                      "Votre nom complet s il vous plait ?")
            return sauver_reponse(reponse)
        else:
            return sauver_reponse("Veuillez choisir :\\n\\n1 - Livraison a domicile\\n2 - Je viens en boutique")

    if etape == ETAPE_NOM:
        commande = db.query(Commande).filter(Commande.conversation_id == conversation.id).first()
        commande.client_nom = message.strip()
        if commande.type_recuperation == "BOUTIQUE":
            commande.prix_total = commande.prix_negocie
        db.commit()
        if commande.type_recuperation == "LIVRAISON":
            return sauver_reponse("Merci " + message.strip() + " ! Votre quartier ou ville de livraison ?")
        else:
            return sauver_reponse("Merci " + message.strip() + " ! Votre numero de telephone ?")

    if etape == ETAPE_QUARTIER:
        commande = db.query(Commande).filter(Commande.conversation_id == conversation.id).first()
        commande.client_quartier = message.strip()
        db.commit()
        return sauver_reponse("Super ! Votre numero de telephone pour le livreur ?")

    if etape == ETAPE_TEL_LIVRAISON:
        commande = db.query(Commande).filter(Commande.conversation_id == conversation.id).first()
        livraison = calculer_frais_livraison(commande.client_quartier or "")
        commande.frais_livraison = livraison["frais"]
        commande.prix_total = commande.prix_negocie + livraison["frais"]
        commande.client_telephone = message.strip()
        db.commit()
        recap = ("Recapitulatif de votre commande :\\n\\n"
                "Produit : " + produit.nom + "\\n"
                "Prix negocie : " + str(int(commande.prix_negocie)) + " FCFA\\n"
                "Livraison " + (commande.client_quartier or "") + " : " + str(int(commande.frais_livraison)) + " FCFA\\n"
                "Total : " + str(int(commande.prix_total)) + " FCFA\\n\\n"
                "Paiement a la livraison\\n\\n"
                "Confirmez-vous ? Repondez OUI pour valider")
        return sauver_reponse(recap)

    if etape == ETAPE_CONFIRMATION:
        commande = db.query(Commande).filter(Commande.conversation_id == conversation.id).first()
        est_tel = bool(re.match(r"^[0-9]{6,12}$", message.strip()))
        if commande.type_recuperation == "BOUTIQUE":
            commande.client_telephone = message.strip()
            numero = generer_numero_facture()
            commande.numero_facture = numero
            commande.statut = "CONFIRMEE"
            conversation.statut = "TERMINEE"
            db.commit()
            return sauver_reponse("Parfait ! Reservation confirmee. Facture N " + numero + "\\nPresentez-vous en boutique avec ce numero. Merci " + commande.client_nom + " !")
        if not est_tel and "oui" in message_lower:
            numero = generer_numero_facture()
            commande.numero_facture = numero
            commande.statut = "CONFIRMEE"
            conversation.statut = "TERMINEE"
            db.commit()
            commande_data = {
                "numero_facture": numero,
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
            try:
                envoyer_facture_client(commande.client_telephone, commande_data)
                envoyer_notification_commercant(client_telephone, commande_data)
            except Exception:
                pass
            reponse = ("Commande confirmee ! Facture N " + numero + " envoyee.\\n\\n"
                      "Notre equipe vous contactera sous 2h pour la livraison.\\n"
                      "Merci " + commande.client_nom + " !")
            return sauver_reponse(reponse)
        else:
            if commande.type_recuperation == "LIVRAISON":
                return sauver_reponse("Recapitulatif :\\nProduit : " + produit.nom + "\\nTotal : " + str(int(commande.prix_total)) + " FCFA\\n\\nConfirmez-vous ? Repondez OUI")
            else:
                return sauver_reponse("Votre numero de telephone pour finaliser ?")

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
    return {
        "conversation_id": conversation.id,
        "reponse_bot": reponse,
        "prix_propose": prix_propose,
        "statut": conversation.statut,
        "prix_final": conversation.prix_final
    }
"""

with open("app/services/negotiation_engine.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Moteur complet ecrit avec succes !")