import re

with open("app/services/negotiation_engine.py", "r", encoding="utf-8") as f:
    code = f.read()

# Voir ce qui est ecrit actuellement autour de la confirmation
idx = code.find("ETAPE : CONFIRMATION")
print("=== EXTRAIT CONFIRMATION ===")
print(code[idx:idx+500])