with open("app/services/negotiation_engine.py", "r", encoding="utf-8") as f:
    code = f.read()

ancien = '''        if commande.type_recuperation == "BOUTIQUE" and not commande.client_telephone:'''
nouveau = '''        if commande.type_recuperation == "BOUTIQUE":'''

if ancien in code:
    code = code.replace(ancien, nouveau)
    with open("app/services/negotiation_engine.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("Correction boutique appliquee !")
else:
    print("Texte non trouve - deja corrige ou different")
    idx = code.find("BOUTIQUE")
    print(repr(code[idx:idx+200]))