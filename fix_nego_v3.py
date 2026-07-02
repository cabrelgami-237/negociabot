code = open("app/services/negotiation_engine.py").read()

# Corriger la fonction generer_reponse_negociation
ancien = '''    else:
        contre = int((produit.prix_affiche + produit.prix_cible) / 2)
        if nb_tours == 0:
            return ("NEGOCIATION", "Bonjour ! Le " + produit.nom + " est a " + str(int(produit.prix_affiche)) + " FCFA. C est de la qualite superieure ! Je peux faire un effort pour vous.")
        else:
            return ("NEGOCIATION", "Hmm " + str(int(prix_propose)) + " FCFA c est un peu juste. Je peux vous faire " + str(contre) + " FCFA, c est mon meilleur effort !")'''

nouveau = '''    else:
        contre = int((produit.prix_affiche + produit.prix_cible) / 2)
        if nb_tours == 0 or prix_propose is None:
            return ("NEGOCIATION", "Bonjour ! Le " + produit.nom + " est a " + str(int(produit.prix_affiche)) + " FCFA. C est de la qualite superieure ! Je peux faire un effort pour vous.")
        else:
            return ("NEGOCIATION", "Hmm " + str(int(prix_propose)) + " FCFA c est un peu juste. Je peux vous faire " + str(contre) + " FCFA, c est mon meilleur effort !")'''

code = code.replace(ancien, nouveau)

with open("app/services/negotiation_engine.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Correction appliquee avec succes !")