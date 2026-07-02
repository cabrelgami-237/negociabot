import uuid
from datetime import datetime
from app.services.whatsapp_service import envoyer_message_whatsapp


def generer_numero_facture() -> str:
    date = datetime.now().strftime("%Y%m%d")
    code = str(uuid.uuid4())[:6].upper()
    return "NB-" + date + "-" + code


def generer_facture_texte(commande_data: dict) -> str:
    numero = commande_data.get("numero_facture", "NB-000000")
    date = datetime.now().strftime("%d/%m/%Y %H:%M")
    client_nom = commande_data.get("client_nom", "")
    client_tel = commande_data.get("client_telephone", "")
    produit_nom = commande_data.get("produit_nom", "")
    prix_negocie = commande_data.get("prix_negocie", 0)
    frais_livraison = commande_data.get("frais_livraison", 0)
    prix_total = commande_data.get("prix_total", 0)
    type_recuperation = commande_data.get("type_recuperation", "LIVRAISON")
    quartier = commande_data.get("client_quartier", "")
    boutique_nom = commande_data.get("boutique_nom", "NegociaBot")

    if type_recuperation == "LIVRAISON":
        livraison_ligne = "Livraison " + quartier + " : " + str(int(frais_livraison)) + " FCFA"
    else:
        livraison_ligne = "Retrait en boutique : Gratuit"

    lignes = [
        "FACTURE NEGOCIABOT",
        "==================",
        "Numero : " + numero,
        "Date   : " + date,
        "",
        "VENDEUR : " + boutique_nom,
        "",
        "CLIENT",
        "------",
        "Nom : " + client_nom,
        "Tel : " + client_tel,
        "",
        "COMMANDE",
        "--------",
        "Produit : " + produit_nom,
        "Prix negocie : " + str(int(prix_negocie)) + " FCFA",
        livraison_ligne,
        "------------------",
        "TOTAL : " + str(int(prix_total)) + " FCFA",
        "",
        "PAIEMENT A LA LIVRAISON",
        "Merci pour votre confiance !"
    ]
    return "\n".join(lignes)


def envoyer_facture_client(telephone_client: str, commande_data: dict):
    facture = generer_facture_texte(commande_data)
    message = "Voici votre facture NegociaBot :\n\n" + facture
    envoyer_message_whatsapp(telephone_client, message)


def envoyer_notification_commercant(telephone_commercant: str, commande_data: dict) -> str:
    type_rec = commande_data.get("type_recuperation", "LIVRAISON")
    client_nom = commande_data.get("client_nom", "")
    client_tel = commande_data.get("client_telephone", "")
    produit_nom = commande_data.get("produit_nom", "")
    prix_negocie = commande_data.get("prix_negocie", 0)
    frais_livraison = commande_data.get("frais_livraison", 0)
    prix_total = commande_data.get("prix_total", 0)
    quartier = commande_data.get("client_quartier", "")
    numero = commande_data.get("numero_facture", "")

    if type_rec == "LIVRAISON":
        type_ligne = "LIVRAISON - " + quartier
        frais_ligne = "Frais livraison : " + str(int(frais_livraison)) + " FCFA"
    else:
        type_ligne = "RETRAIT EN BOUTIQUE"
        frais_ligne = "Frais livraison : 0 FCFA"

    lignes = [
        "NOUVELLE COMMANDE NegociaBot !",
        "Facture : " + numero,
        "",
        "CLIENT",
        "Nom : " + client_nom,
        "Tel : " + client_tel,
        "",
        "COMMANDE",
        "Produit : " + produit_nom,
        "Prix negocie : " + str(int(prix_negocie)) + " FCFA",
        frais_ligne,
        "TOTAL : " + str(int(prix_total)) + " FCFA",
        "",
        "TYPE : " + type_ligne,
        "",
        "PAIEMENT A LA LIVRAISON",
        "Action : Preparez la commande !"
    ]
    message = "\n".join(lignes)
    envoyer_message_whatsapp(telephone_commercant, message)
    return message
