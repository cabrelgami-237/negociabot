code = open("app/services/negotiation_engine.py").read()

# Corriger : le telephone collecte ne doit pas declencher la confirmation
ancien = '''    # ETAPE : COLLECTE TELEPHONE
    if etape == ETAPES["COLLECTE_TELEPHONE"]:
        commande = db.query(Commande).filter(Commande.conversation_id == conversation.id).first()
        commande.client_telephone = message.strip()
        db.commit()'''

nouveau = '''    # ETAPE : COLLECTE TELEPHONE
    if etape == ETAPES["COLLECTE_TELEPHONE"]:
        commande = db.query(Commande).filter(Commande.conversation_id == conversation.id).first()
        # Stocker le telephone de livraison (different du telephone WhatsApp)
        commande.client_telephone = message.strip()
        db.commit()
        # Forcer l etape suivante vers CONFIRMATION, pas vers annulation'''

code = code.replace(ancien, nouveau)

# Corriger aussi la condition de confirmation pour etre plus stricte
ancien2 = '''        if "oui" in message_lower or "yes" in message_lower or "ok" in message_lower or "confirme" in message_lower:'''

nouveau2 = '''        # Verifier que ce n est pas un numero de telephone
        est_telephone = bool(__import__("re").match(r"^[0-9]{6,12}$", message.strip()))
        if not est_telephone and ("oui" in message_lower or "yes" in message_lower or "ok" in message_lower or "confirme" in message_lower or "d accord" in message_lower):'''

code = code.replace(ancien2, nouveau2)

with open("app/services/negotiation_engine.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Correction etapes appliquee !")