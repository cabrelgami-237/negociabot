from passlib.context import CryptContext
from sqlalchemy import create_engine, text

RENDER_URL = "postgresql://negociabot_db_user:x9Xqi0LnM0q22pQDwuNcPpth5oUM2GE2@dpg-d95n6hvaqgkc73fb844g-a.frankfurt-postgres.render.com/negociabot_db"

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
nouveau_hash = pwd_ctx.hash("NouveauMDP2026")
print("Hash genere OK")

engine = create_engine(RENDER_URL)
with engine.connect() as conn:
    result = conn.execute(text("SELECT email, abonnement_actif FROM commercants"))
    rows = result.fetchall()
    print("Comptes en base Render:")
    for r in rows:
        print(f"  - {r[0]} | actif: {r[1]}")

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
        print(f"\nMise a jour Render reussie!")
        print(f"Email: {row[0]} | actif: {row[1]}")
        print(f"\nConnecte-toi avec:")
        print(f"  Email   : cabrelgami@gmail.com")
        print(f"  Password: NouveauMDP2026")
    else:
        print("COMPTE NON TROUVE sur Render")