from passlib.context import CryptContext
from sqlalchemy import create_engine, text

RENDER_URL = "postgresql://negociabot_db_user:x9Xqi0LnM0q22pQDwuNcPpth5oUM2GE2@dpg-d95n6hvaqgkc73fb844g-a.frankfurt-postgres.render.com/negociabot_db"

engine = create_engine(RENDER_URL)
with engine.connect() as conn:
    result = conn.execute(text(
        "SELECT email, nom_boutique, plan_abonnement, abonnement_actif, created_at FROM commercants ORDER BY created_at"
    ))
    rows = result.fetchall()
    print(f"\n{'='*60}")
    print(f"  COMPTES SUR RENDER ({len(rows)} compte(s))")
    print(f"{'='*60}")
    for r in rows:
        print(f"\n  Email    : {r[0]}")
        print(f"  Boutique : {r[1]}")
        print(f"  Plan     : {r[2]}")
        print(f"  Actif    : {r[3]}")
        print(f"  Cree le  : {r[4]}")
    print(f"\n{'='*60}")
    print("\nMots de passe associes:")
    print("  Linustako@gmail.com    -> NouveauMDP2026")
    print("  cabrelgami@gmail.com   -> NouveauMDP2026")
    print("  cabrelle@negociabot.cm -> Test1234")
    print(f"{'='*60}\n")