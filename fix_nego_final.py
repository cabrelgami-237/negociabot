code = open("app/services/negotiation_engine.py", encoding="utf-8").read()

ancien = '''        if "oui" in message_lower or "yes" in message_lower or "ok" in message_lower or "confirme" in message_lower:'''

nouveau = '''        import re as _re
        est_telephone = bool(_re.match(r"^[0-9]{6,12}$", message.strip()))
        if not est_telephone and ("oui" in message_lower or "yes" in message_lower or "ok" in message_lower or "confirme" in message_lower or "d accord" in message_lower):'''

code = code.replace(ancien, nouveau)

with open("app/services/negotiation_engine.py", "w", encoding="utf-8") as f:
    f.write(code)
print("Correction appliquee !")