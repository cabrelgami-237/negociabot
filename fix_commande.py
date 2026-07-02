import os

# ===== app/models/commande.py =====
commande_model = """from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base
import uuid

class Commande(Base):
    __tablename__ = "commandes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    commercant_id = Column(String, ForeignKey("commercants.id"), nullable=False)
    produit_id = Column(String, ForeignKey("produits.id"), nullable=False)
    client_nom = Column(String, nullable=False)
    client_telephone = Column(String, nullable=False)
    client_quartier = Column(String, nullable=True)
    client_ville = Column(String, nullable=True)
    type_recuperation = Column(String, default="LIVRAISON")  # LIVRAISON ou BOUTIQUE
    prix_negocie = Column(Float, nullable=False)
    frais_livraison = Column(Float, default=0)
    prix_total = Column(Float, nullable=False)
    statut = Column(String, default="EN_ATTENTE")  # EN_ATTENTE, CONFIRMEE, LIVREE, ANNULEE
    numero_facture = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
"""

# ===== app/schemas/commande.py =====
commande_schema = """from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommandeCreate(BaseModel):
    conversation_id: str
    commercant_id: str
    produit_id: str
    client_nom: str
    client_telephone: str
    client_quartier: Optional[str] = None
    client_ville: Optional[str] = None
    type_recuperation: str  # LIVRAISON ou BOUTIQUE
    prix_negocie: float

class CommandeResponse(BaseModel):
    id: str
    conversation_id: str
    commercant_id: str
    produit_id: str
    client_nom: str
    client_telephone: str
    client_quartier: Optional[str] = None
    client_ville: Optional[str] = None
    type_recuperation: str
    prix_negocie: float
    frais_livraison: float
    prix_total: float
    statut: str
    numero_facture: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
"""

# ===== app/services/livraison_service.py =====
livraison_service = """# Zones de livraison pour Douala et autres villes

ZONES_DOUALA = {
    "zone1": {
        "quartiers": ["akwa", "bonanjo", "bali", "new bell", "centre", "cite des palmiers"],
        "prix": 500,
        "description": "Centre-ville Douala"
    },
    "zone2": {
        "quartiers": ["makepe", "bonapriso", "deido", "bonaberi", "mboppi", "bessengue"],
        "prix": 1000,
        "description": "Douala proche"
    },
    "zone3": {
        "quartiers": ["logbessou", "pk", "ndokotti", "nyalla", "village", "cam rail", "bepanda"],
        "prix": 1500,
        "description": "Douala eloigne"
    },
    "zone4": {
        "quartiers": ["kotto", "yassa", "japoma", "bonaberi", "dibamba", "ngodi"],
        "prix": 2000,
        "description": "Peripherie Douala"
    }
}

VILLES_CAMEROUN = {
    "yaounde": 5000,
    "bafoussam": 6000,
    "garoua": 8000,
    "maroua": 10000,
    "bamenda": 6000,
    "limbe": 3000,
    "kribi": 4000,
    "ebolowa": 5000,
    "bertoua": 7000,
    "ngaoundere": 9000
}


def calculer_frais_livraison(quartier: str, ville: str = "douala") -> dict:
    ville_lower = ville.lower().strip()
    quartier_lower = quartier.lower().strip()

    if ville_lower == "douala" or ville_lower == "":
        for zone_name, zone_info in ZONES_DOUALA.items():
            for q in zone_info["quartiers"]:
                if q in quartier_lower or quartier_lower in q:
                    return {
                        "frais": zone_info["prix"],
                        "zone": zone_name,
                        "description": zone_info["description"],
                        "delai": "2-4 heures"
                    }
        return {
            "frais": 2000,
            "zone": "zone_inconnue",
            "description": "Zone non repertoriee - Douala",
            "delai": "A confirmer"
        }

    for ville_name, prix in VILLES_CAMEROUN.items():
        if ville_name in ville_lower or ville_lower in ville_name:
            return {
                "frais": prix,
                "zone": "hors_douala",
                "description": ville.capitalize(),
                "delai": "24-48 heures"
            }

    return {
        "frais": 0,
        "zone": "sur_devis",
        "description": "Livraison sur devis",
        "delai": "A confirmer"
    }


def get_adresse_boutique(commercant_id: str = None) -> dict:
    return {
        "adresse": "Akwa, Rue 470 Gallieni, Douala",
        "horaires": "Lundi - Samedi : 10h00 - 18h00",
        "telephone": "+237 699 001 122",
        "indication": "En face de la pharmacie centrale"
    }
"""

# ===== app/services/facture_service.py =====
facture_service = """import uuid
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
        livraison_ligne = "Livraison : " + quartier + " - " + str(int(frais_livraison)) + " FCFA"
    else:
        livraison_ligne = "Recuperation : En boutique (gratuit)"

    facture = """
FACTURE NEGOCIABOT
==================
Numero : """ + numero + """
Date : """ + date + """

VENDEUR
-------
Boutique : """ + boutique_nom + """

CLIENT
------
Nom : """ + client_nom + """
Tel : """ + client_tel + """

COMMANDE
--------
Produit : """ + produit_nom + """
Prix negocie : """ + str(int(prix_negocie)) + """ FCFA
""" + livraison_ligne + """
------------------
TOTAL : """ + str(int(prix_total)) + """ FCFA

PAIEMENT A LA LIVRAISON
========================
Merci pour votre confiance !
"""
    return facture


def envoyer_facture_client(telephone_client: str, commande_data: dict):
    facture = generer_facture_texte(commande_data)
    message = "Voici votre facture NegociaBot :" + facture
    envoyer_message_whatsapp(telephone_client, message)


def envoyer_notification_commercant(telephone_commercant: str, commande_data: dict):
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

    message = """NOUVELLE COMMANDE NegociaBot !
Facture : """ + numero + """

CLIENT
------
Nom : """ + client_nom + """
Tel : """ + client_tel + """

COMMANDE
--------
Produit : """ + produit_nom + """
Prix negocie : """ + str(int(prix_negocie)) + """ FCFA
""" + frais_ligne + """
TOTAL : """ + str(int(prix_total)) + """ FCFA

TYPE : """ + type_ligne + """

PAIEMENT A LA LIVRAISON
Action requise : Preparez la commande !"""

    envoyer_message_whatsapp(telephone_commercant, message)
    return message
"""

# ===== Ecriture des fichiers =====
files = {
    "app/models/commande.py": commande_model,
    "app/schemas/commande.py": commande_schema,
    "app/services/livraison_service.py": livraison_service,
    "app/services/facture_service.py": facture_service,
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Ecrit : " + path)

print("Tous les fichiers crees avec succes !")