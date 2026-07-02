with open("app/services/negotiation_engine.py", "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("type_recuperation == \"BOUTIQUE\"")
print("=== BOUTIQUE ===")
print(code[idx:idx+200])