from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    mot_de_passe: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "cabrelle@negociabot.cm",
                "mot_de_passe": "Test1234"
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    commercant_id: str
    nom_boutique: str
    plan_abonnement: str
    message: str = "Connexion reussie"


class TokenData(BaseModel):
    commercant_id: str | None = None
    email: str | None = None


class RegisterRequest(BaseModel):
    nom_boutique: str
    email: EmailStr
    telephone: str
    mot_de_passe: str
    domaine_activite: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "nom_boutique": "Boutique Exemple",
                "email": "nouveau@negociabot.cm",
                "telephone": "+237600000000",
                "mot_de_passe": "MotDePasse123",
                "domaine_activite": "Vente en ligne"
            }
        }


class RegisterResponse(BaseModel):
    commercant_id: str
    nom_boutique: str
    email: str
    plan_abonnement: str
    message: str = "Compte cree avec succes"