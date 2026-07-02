from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import auth, commercants, abonnements, produits, negotiation, dashboard, paiement, whatsapp
from app.database.database import Base, engine
from app.models import commercant, produit, conversation, abonnement, commande

# Creer les tables automatiquement
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NegociaBot API",
    description="Systeme IA de negociation - Cameroun",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(commercants.router)
app.include_router(abonnements.router)
app.include_router(produits.router)
app.include_router(negotiation.router)
app.include_router(dashboard.router)
app.include_router(paiement.router)
app.include_router(whatsapp.router)


@app.get("/")
def root():
    return {
        "projet": "NegociaBot",
        "version": "4.0.0",
        "statut": "actif",
        "message": "Bot de negociation IA operationnel !",
        "nouveautes": [
            "Negociation naturelle amelioree",
            "Collecte infos client apres accord",
            "Calcul frais livraison par zone Douala",
            "Option retrait en boutique",
            "Generation facture automatique",
            "Notification commercant WhatsApp"
        ]
    }


@app.get("/health")
def health():
    return {"statut": "ok"}
