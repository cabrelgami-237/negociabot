ZONES_DOUALA = {
    "zone1": {
        "quartiers": ["akwa", "bonanjo", "bali", "new bell", "centre", "cite des palmiers"],
        "prix": 500,
        "description": "Centre-ville Douala"
    },
    "zone2": {
        "quartiers": ["makepe", "bonapriso", "deido", "mboppi", "bessengue"],
        "prix": 1000,
        "description": "Douala proche"
    },
    "zone3": {
        "quartiers": ["logbessou", "pk", "ndokotti", "nyalla", "bepanda", "cam rail"],
        "prix": 1500,
        "description": "Douala eloigne"
    },
    "zone4": {
        "quartiers": ["kotto", "yassa", "japoma", "bonaberi", "dibamba", "ngodi"],
        "prix": 2000,
        "description": "Peripherie Douala"
    }
}

VILLES_CAMEROUN = {
    "yaounde": 5000,
    "bafoussam": 6000,
    "garoua": 8000,
    "maroua": 10000,
    "bamenda": 6000,
    "limbe": 3000,
    "kribi": 4000,
    "ebolowa": 5000,
    "bertoua": 7000,
    "ngaoundere": 9000
}


def calculer_frais_livraison(quartier: str, ville: str = "douala") -> dict:
    ville_lower = ville.lower().strip()
    quartier_lower = quartier.lower().strip()

    if ville_lower == "douala" or ville_lower == "":
        for zone_name, zone_info in ZONES_DOUALA.items():
            for q in zone_info["quartiers"]:
                if q in quartier_lower or quartier_lower in q:
                    return {
                        "frais": zone_info["prix"],
                        "zone": zone_name,
                        "description": zone_info["description"],
                        "delai": "2-4 heures"
                    }
        return {
            "frais": 2000,
            "zone": "zone_inconnue",
            "description": "Zone non repertoriee",
            "delai": "A confirmer"
        }

    for ville_name, prix in VILLES_CAMEROUN.items():
        if ville_name in ville_lower or ville_lower in ville_name:
            return {
                "frais": prix,
                "zone": "hors_douala",
                "description": ville.capitalize(),
                "delai": "24-48 heures"
            }

    return {
        "frais": 0,
        "zone": "sur_devis",
        "description": "Livraison sur devis",
        "delai": "A confirmer"
    }


def get_adresse_boutique() -> dict:
    return {
        "adresse": "Akwa, Rue 470 Gallieni, Douala",
        "horaires": "Lundi - Samedi : 10h00 - 18h00",
        "telephone": "+237 699 001 122",
        "indication": "En face de la pharmacie centrale"
    }
