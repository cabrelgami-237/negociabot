# app/services/gemini_service.py
"""
Service Gemini AI - Reformulation naturelle des reponses de negociation.

Architecture :
- Le moteur a regles DECIDE (accepter, refuser, contre-offre, montants).
- Gemini REFORMULE la decision en langage naturel camerounais.
- En cas d'erreur Gemini (quota, reseau, cle absente), on retourne
  la reponse brute du moteur : le bot ne tombe jamais en panne.
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"  # gratuit, modele actuellement disponible

_client = None


def _get_client():
    """Initialise le client Gemini une seule fois (lazy loading)."""
    global _client
    if _client is None and GEMINI_API_KEY:
        try:
            from google import genai
            _client = genai.Client(api_key=GEMINI_API_KEY)
            logger.info("Client Gemini initialise avec succes")
        except Exception as e:
            logger.error("Impossible d'initialiser Gemini: %s", e)
    return _client


def gemini_disponible() -> bool:
    """Verifie si Gemini est configure et utilisable."""
    return bool(GEMINI_API_KEY) and _get_client() is not None


def reformuler_reponse(
    message_client,
    reponse_moteur,
    nom_produit,
    prix_affiche,
    prix_propose,
    contre_offre,
    decision,
    historique=None,
):
    """
    Reformule la reponse du moteur a regles en langage naturel.

    Args:
        message_client: dernier message du client (str)
        reponse_moteur: reponse generee par le moteur a regles (str, fallback)
        nom_produit: nom du produit negocie (str)
        prix_affiche: prix affiche du produit en FCFA (float)
        prix_propose: prix propose par le client en FCFA (float ou None)
        contre_offre: contre-offre du moteur en FCFA (float ou None)
        decision: 'accueil', 'contre_offre', 'derniere_offre' ou 'refus'
        historique: liste de dicts [{'role': 'client'|'bot', 'contenu': str}]

    Returns:
        str: reponse naturelle, ou reponse_moteur si Gemini indisponible.
    """
    client = _get_client()
    if client is None:
        return reponse_moteur

    # Construire le contexte des derniers echanges
    contexte_hist = ""
    if historique:
        lignes = []
        for msg in historique[-6:]:
            role = "Client" if msg.get("role") == "client" else "Vendeur"
            lignes.append(role + ": " + str(msg.get("contenu", "")))
        contexte_hist = "\n".join(lignes)

    system_instruction = (
        "Tu es un vendeur camerounais sympathique et professionnel sur WhatsApp, "
        "a Douala. Tu negocies le prix d'un produit avec un client. "
        "Tu reponds en francais simple et chaleureux, avec le ton du commerce "
        "camerounais (poli, un peu familier, sans exces). "
        "REGLES STRICTES :\n"
        "1. Tu ne changes JAMAIS les montants donnes dans la decision.\n"
        "2. Tu ne proposes JAMAIS un autre prix que celui indique.\n"
        "3. Tu n'acceptes et ne refuses JAMAIS de toi-meme : tu suis la decision.\n"
        "4. Reponse courte : 1 a 3 phrases maximum, adaptee a WhatsApp.\n"
        "5. Au plus 1 emoji.\n"
        "6. Tous les prix sont en FCFA."
    )

    infos_offre = "aucune offre chiffree"
    if prix_propose:
        infos_offre = str(int(prix_propose)) + " FCFA"

    ligne_contre = ""
    if contre_offre:
        ligne_contre = "Contre-offre a proposer au client : " + str(int(contre_offre)) + " FCFA\n"

    prompt = (
        "Produit : " + nom_produit + "\n"
        "Prix affiche : " + str(int(prix_affiche)) + " FCFA\n"
        "Offre du client : " + infos_offre + "\n\n"
        "Historique recent :\n"
        + (contexte_hist if contexte_hist else "(debut de conversation)") + "\n\n"
        'Dernier message du client : "' + message_client + '"\n\n'
        "Decision du systeme : " + decision + "\n"
        + ligne_contre +
        'Message de base a reformuler : "' + reponse_moteur + '"\n\n'
        "Reformule ce message de facon naturelle et chaleureuse, en respectant "
        "exactement la decision et les montants. Reponds UNIQUEMENT avec le "
        "message a envoyer au client, rien d'autre."
    )

    try:
        from google.genai import types
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=200,
            ),
        )
        texte = (response.text or "").strip()
        if texte:
            return texte
        logger.warning("Gemini a retourne une reponse vide, fallback moteur")
        return reponse_moteur
    except Exception as e:
        logger.error("Erreur Gemini, fallback sur le moteur a regles: %s", e)
        return reponse_moteur