with open("app/services/negotiation_engine.py", "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("ETAPE : COLLECTE TELEPHONE")
print("=== COLLECTE TELEPHONE ===")
print(code[idx:idx+600])
