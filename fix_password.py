from passlib.context import CryptContext
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
nouveau_hash = pwd.hash("NouveauMDP2026")
print("Nouveau hash genere OK")

database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("ERREUR: DATABASE_URL vide dans .env")
    exit(1)

print("Connexion a:", database_url[:30], "...")

engine = create_engine(database_url)

with engine.connect() as conn:
    result = conn.execute(text("SELECT email, abonnement_actif, mot_de_passe_hash FROM commercants"))
    rows = result.fetchall()

    if not rows:
        print("AUCUN COMPTE TROUVE EN BASE")
    else:
        print("Comptes trouves en base:")
        for r in rows:
            hash_val = r[2] if r[2] else "VIDE"
            valide = hash_val.startswith("$2b$") if hash_val != "VIDE" else False
            print(f"  - {r[0]} | actif: {r[1]} | hash valide: {valide}")

    conn.execute(
        text("UPDATE commercants SET mot_de_passe_hash = :h, abonnement_actif = true WHERE email = 'cabrelgami@gmail.com'"),
        {"h": nouveau_hash}
    )
    conn.commit()

    result2 = conn.execute(
        text("SELECT email, abonnement_actif FROM commercants WHERE email = 'cabrelgami@gmail.com'")
    )
    row = result2.fetchone()
    if row:
        print(f"\nMise a jour reussie!")
        print(f"Email: {row[0]}")
        print(f"Abonnement actif: {row[1]}")
        print(f"\nConnecte-toi avec:")
        print(f"  Email: cabrelgami@gmail.com")
        print(f"  Mot de passe: NouveauMDP2026")
    else:
        print("COMPTE NON TROUVE - email cabrelgami@gmail.com inexistant en base")