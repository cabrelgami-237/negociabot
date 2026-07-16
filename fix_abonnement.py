from app.database.database import SessionLocal
from app.models.commercant import Commercant

db = SessionLocal()

commercant = db.query(Commercant).filter(
    Commercant.email == "Linustako@gmail.com"
).first()

if commercant:
    commercant.abonnement_actif = True
    db.commit()
    print(f"Compte {commercant.email} activé avec succès.")
else:
    print("Compte introuvable.")

db.close()