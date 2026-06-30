\# 🤝 NégociaBot — Bot de Négociation IA pour le Cameroun



> Système SaaS de négociation automatique par intelligence artificielle, conçu pour les commerçants camerounais.



\## 🇨🇲 Contexte



NégociaBot permet aux commerçants de publier leurs produits sur Facebook, Instagram ou WhatsApp, et de laisser un bot IA négocier automatiquement les prix avec les clients — 24h/24, 7j/7, sans intervention humaine.



\## ✨ Fonctionnalités



\- 🔐 Authentification JWT sécurisée

\- 📦 Gestion des produits avec prix affiché, cible et plancher

\- 🤖 Moteur de négociation IA (stratégies : NEGOCIER, ACCEPTER, REFUSER, DERNIERE\_OFFRE)

\- 💬 Intégration WhatsApp Business (webhook)

\- 🔗 Click-to-WhatsApp pour Facebook et Instagram

\- 💳 Paiement MTN Mobile Money

\- 💳 Paiement Orange Money

\- 📊 Tableau de bord avec statistiques en temps réel

\- 🌐 Interface web React moderne



\## 🛠️ Technologies



| Couche | Technologie |

|--------|------------|

| Backend | FastAPI (Python) |

| Base de données | PostgreSQL 17 |

| Authentification | JWT (Jose) |

| Frontend | React.js |

| Paiement | MTN MoMo + Orange Money |

| Messagerie | WhatsApp Business API |



\## 🚀 Installation



\### Backend



```bash

cd app

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

uvicorn app.main:app --reload

```



\### Frontend



```bash

cd negociabot-frontend

npm install

npm start

```



\### Variables d'environnement (.env)



```env

SECRET\_KEY=negociabot-secret-key-cameroun-2026

ALGORITHM=HS256

ACCESS\_TOKEN\_EXPIRE\_MINUTES=30

DATABASE\_URL=postgresql://postgres:motdepasse@localhost:5432/negociabot\_db

OPENAI\_API\_KEY=optionnel

WHATSAPP\_TOKEN=optionnel

WHATSAPP\_PHONE\_ID=optionnel

MOMO\_SUBSCRIPTION\_KEY=optionnel

ORANGE\_CLIENT\_ID=optionnel

ORANGE\_CLIENT\_SECRET=optionnel

```



\## 📱 Comment ça marche



1\. Le commerçant ajoute ses produits avec 3 prix (affiché, cible, plancher)

2\. Il génère un lien WhatsApp depuis la page Produits

3\. Il colle ce lien dans ses publications Facebook/Instagram

4\. Le client clique → WhatsApp s'ouvre → NégociaBot négocie automatiquement

5\. Le commerçant suit tout depuis son tableau de bord



\## 📊 Architecture

