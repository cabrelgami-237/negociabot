from passlib.context import CryptContext
from sqlalchemy import create_engine, text
import uuid

RENDER_URL = "postgresql://negociabot_db_user:x9Xqi0LnM0q22pQDwuNcPpth5oUM2GE2@dpg-d95n6hvaqgkc73fb844g-a.frankfurt-postgres.render.com/negociabot_db"

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Comptes a creer
comptes = [
    {
        "email": "cabrelgami@gmail.com",
        "mot_de_passe": "NouveauMDP2026",
        "nom_boutique": "Boutique Cabrelle",
        "plan": "BUSINESS"
    },
    {
        "email": "cabrelle@negociabot.cm",
        "mot_de_passe": "Test1234",
        "nom_boutique": "Boutique Wax Cabrelle",
        "plan": "BUSINESS"
    }
]

engine = create_engine(RENDER_URL)
with engine.connect() as conn:
    # Voir la structure de la table
    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'commercants' ORDER BY ordinal_position"))
    colonnes = [r[0] for r in result.fetchall()]
    print("Colonnes de la table commercants:", colonnes)

    # Voir les comptes existants
    result2 = conn.execute(text("SELECT email, abonnement_actif, plan_abonnement FROM commercants"))
    rows = result2.fetchall()
    print("\nComptes existants:")
    for r in rows:
        print(f"  - {r[0]} | actif: {r[1]} | plan: {r[2]}")

    # Mettre a jour Linustako aussi
    hash_linus = pwd_ctx.hash("NouveauMDP2026")
    conn.execute(
        text("UPDATE commercants SET mot_de_passe_hash = :h, abonnement_actif = true WHERE email = 'Linustako@gmail.com'"),
        {"h": hash_linus}
    )
    conn.commit()
    print("\nLinustako@gmail.com mis a jour avec NouveauMDP2026")

    # Creer les comptes manquants
    emails_existants = [r[0].lower() for r in rows]
    for compte in comptes:
        if compte["email"].lower() not in emails_existants:
            nouveau_hash = pwd_ctx.hash(compte["mot_de_passe"])
            new_id = str(uuid.uuid4())

            # Essayer avec les colonnes disponibles
            try:
                conn.execute(
                    text("""INSERT INTO commercants (id, email, mot_de_passe_hash, nom_boutique, plan_abonnement, abonnement_actif)
                            VALUES (:id, :email, :hash, :nom, :plan, true)"""),
                    {
                        "id": new_id,
                        "email": compte["email"],
                        "hash": nouveau_hash,
                        "nom": compte["nom_boutique"],
                        "plan": compte["plan"]
                    }
                )
                conn.commit()
                print(f"Compte cree: {compte['email']}")
            except Exception as e:
                print(f"Erreur creation {compte['email']}: {e}")
        else:
            # Mettre a jour si existe
            nouveau_hash = pwd_ctx.hash(compte["mot_de_passe"])
            conn.execute(
                text("UPDATE commercants SET mot_de_passe_hash = :h, abonnement_actif = true WHERE LOWER(email) = :email"),
                {"h": nouveau_hash, "email": compte["email"].lower()}
            )
            conn.commit()
            print(f"Compte mis a jour: {compte['email']}")

    print("\n=== RESUME FINAL ===")
    print("Tu peux te connecter avec:")
    print("  Email: Linustako@gmail.com | MDP: NouveauMDP2026")
    print("  Email: cabrelgami@gmail.com | MDP: NouveauMDP2026 (si cree)")
    print("  Email: cabrelle@negociabot.cm | MDP: Test1234 (si cree)")