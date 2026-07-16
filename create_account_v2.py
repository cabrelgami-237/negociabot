from passlib.context import CryptContext
from sqlalchemy import create_engine, text
import uuid

RENDER_URL = "postgresql://negociabot_db_user:x9Xqi0LnM0q22pQDwuNcPpth5oUM2GE2@dpg-d95n6hvaqgkc73fb844g-a.frankfurt-postgres.render.com/negociabot_db"

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

comptes = [
    {
        "email": "cabrelgami@gmail.com",
        "mot_de_passe": "NouveauMDP2026",
        "nom_boutique": "Boutique Cabrelle",
        "telephone": "699000001",
        "plan": "BUSINESS"
    },
    {
        "email": "cabrelle@negociabot.cm",
        "mot_de_passe": "Test1234",
        "nom_boutique": "Boutique Wax Cabrelle",
        "telephone": "699000002",
        "plan": "BUSINESS"
    }
]

engine = create_engine(RENDER_URL)
with engine.connect() as conn:
    result = conn.execute(text("SELECT email, abonnement_actif FROM commercants"))
    rows = result.fetchall()
    emails_existants = [r[0].lower() for r in rows]
    print("Comptes existants:", [r[0] for r in rows])

    for compte in comptes:
        nouveau_hash = pwd_ctx.hash(compte["mot_de_passe"])
        if compte["email"].lower() in emails_existants:
            conn.execute(
                text("UPDATE commercants SET mot_de_passe_hash=:h, abonnement_actif=true WHERE LOWER(email)=:e"),
                {"h": nouveau_hash, "e": compte["email"].lower()}
            )
            conn.commit()
            print(f"Mis a jour : {compte['email']}")
        else:
            conn.execute(
                text("""INSERT INTO commercants
                    (id, email, mot_de_passe_hash, nom_boutique, telephone, plan_abonnement, abonnement_actif)
                    VALUES (:id, :email, :hash, :nom, :tel, :plan, true)"""),
                {
                    "id": str(uuid.uuid4()),
                    "email": compte["email"],
                    "hash": nouveau_hash,
                    "nom": compte["nom_boutique"],
                    "tel": compte["telephone"],
                    "plan": compte["plan"]
                }
            )
            conn.commit()
            print(f"Cree : {compte['email']}")

    print("\n=== COMPTES FINAUX SUR RENDER ===")
    result2 = conn.execute(text("SELECT email, abonnement_actif, plan_abonnement FROM commercants"))
    for r in result2.fetchall():
        print(f"  {r[0]} | actif: {r[1]} | plan: {r[2]}")

    print("\n=== CONNECTE-TOI AVEC ===")
    print("  Email: Linustako@gmail.com    | MDP: NouveauMDP2026")
    print("  Email: cabrelgami@gmail.com   | MDP: NouveauMDP2026")
    print("  Email: cabrelle@negociabot.cm | MDP: Test1234")