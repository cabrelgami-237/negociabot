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