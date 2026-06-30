from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.produit import Produit
from app.schemas.produit import ProduitCreate, ProduitResponse, ProduitUpdate

router = APIRouter(prefix="/produits", tags=["Produits"])


@router.post("/{commercant_id}", response_model=ProduitResponse, status_code=201)
def creer_produit(
    commercant_id: str,
    data: ProduitCreate,
    db: Session = Depends(get_db)
):
    nouveau_produit = Produit(
        commercant_id=commercant_id,
        nom=data.nom,
        description=data.description,
        categorie=data.categorie,
        prix_affiche=data.prix_affiche,
        prix_cible=data.prix_cible,
        prix_plancher=data.prix_plancher,
        devise=data.devise or "FCFA"
    )
    db.add(nouveau_produit)
    db.commit()
    db.refresh(nouveau_produit)
    return nouveau_produit


@router.get("/{commercant_id}", response_model=List[ProduitResponse])
def obtenir_produits(
    commercant_id: str,
    db: Session = Depends(get_db)
):
    produits = db.query(Produit).filter(
        Produit.commercant_id == commercant_id,
        Produit.actif == True
    ).all()
    return produits


@router.get("/detail/{produit_id}", response_model=ProduitResponse)
def obtenir_produit(
    produit_id: str,
    db: Session = Depends(get_db)
):
    produit = db.query(Produit).filter(
        Produit.id == produit_id
    ).first()
    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit introuvable"
        )
    return produit


@router.put("/modifier/{produit_id}", response_model=ProduitResponse)
def modifier_produit(
    produit_id: str,
    data: ProduitUpdate,
    db: Session = Depends(get_db)
):
    produit = db.query(Produit).filter(
        Produit.id == produit_id
    ).first()
    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit introuvable"
        )
    for champ, valeur in data.dict(exclude_unset=True).items():
        setattr(produit, champ, valeur)
    db.commit()
    db.refresh(produit)
    return produit


@router.delete("/supprimer/{produit_id}")
def supprimer_produit(
    produit_id: str,
    db: Session = Depends(get_db)
):
    produit = db.query(Produit).filter(
        Produit.id == produit_id
    ).first()
    if not produit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit introuvable"
        )
    produit.actif = False
    db.commit()
    return {"message": "Produit supprimé avec succès"}