with open("app/services/negotiation_engine.py", "r", encoding="utf-8") as f:
    code = f.read()

# Corriger get_etape_conversation pour utiliser client_quartier comme indicateur
ancien = '''    if commande.statut == "EN_ATTENTE":
        if not commande.type_recuperation or commande.type_recuperation == "":
            return ETAPES["CHOIX_RECUPERATION"]
        if not commande.client_nom or commande.client_nom == "":
            return ETAPES["COLLECTE_NOM"]
        if commande.type_recuperation == "LIVRAISON" and (not commande.client_quartier or commande.client_quartier == ""):
            return ETAPES["COLLECTE_QUARTIER"]
        if not commande.client_telephone or commande.client_telephone == "":
            return ETAPES["COLLECTE_TELEPHONE"]
        return ETAPES["CONFIRMATION"]'''

nouveau = '''    if commande.statut == "EN_ATTENTE":
        if not commande.type_recuperation or commande.type_recuperation == "":
            return ETAPES["CHOIX_RECUPERATION"]
        if not commande.client_nom or commande.client_nom == "":
            return ETAPES["COLLECTE_NOM"]
        if commande.type_recuperation == "LIVRAISON" and (not commande.client_quartier or commande.client_quartier == ""):
            return ETAPES["COLLECTE_QUARTIER"]
        if commande.frais_livraison == 0 and commande.type_recuperation == "LIVRAISON" and commande.client_quartier:
            return ETAPES["COLLECTE_TELEPHONE"]
        if commande.prix_total == commande.prix_negocie and commande.type_recuperation == "LIVRAISON":
            return ETAPES["COLLECTE_TELEPHONE"]
        return ETAPES["CONFIRMATION"]'''

if ancien in code:
    code = code.replace(ancien, nouveau)
    with open("app/services/negotiation_engine.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Correction appliquee !")
else:
    print("Texte non trouve")
    idx = code.find("if commande.statut")
    print(repr(code[idx:idx+500]))