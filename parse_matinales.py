#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re
from datetime import datetime

def parse_date(date_str):
    """Convertit DD/MM/YY en YYYY-MM-DD"""
    parts = date_str.split('/')
    if len(parts) == 3:
        day, month, year = parts
        # Ajoute 20 devant l'année si elle est sur 2 chiffres
        if len(year) == 2:
            year = '20' + year
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    return date_str

def parse_invites_multiples(personne_info):
    """Sépare plusieurs invités séparés par 'et' ou ','"""
    invites = []

    # Nettoyer les points de suspension à la fin
    personne_info = personne_info.rstrip('…').rstrip('.').strip()

    # Pattern pour détecter plusieurs invités :
    # - Séparés par " et " MAIS seulement si suivi d'un nom propre (Prénom Nom)
    # - OU séparés par ", " suivi d'un nom propre avec majuscule (Prénom Nom)

    # D'abord chercher les " et " suivis d'un Prénom Nom (2 mots avec majuscules)
    # Pattern : " et " suivi de Majuscule + word characters + espace + Majuscule
    # Utilisation de \w pour capturer tous les caractères unicode (y compris ï, ü, etc.)
    parties = re.split(r'\s+et\s+(?=[A-ZÉÈÀÊÂÔÛÇÏÜ]\w+\s+[A-ZÉÈÀÊÂÔÛÇÏÜ])', personne_info)

    for partie in parties:
        partie = partie.strip()
        if not partie:
            continue

        # Chercher pattern "Nom Prénom, titre/fonction, Nom2 Prénom2, fonction2"
        # Pattern pour détecter : virgule + espace + Prénom Nom (2 mots avec majuscules au début)
        # On utilise un lookahead pour ne diviser que si c'est suivi d'un nom propre complet
        sub_parties = re.split(r',\s+(?=[A-ZÉÈÀÊÂÔÛÇÏÜ]\w+\s+[A-ZÉÈÀÊÂÔÛÇÏÜ]\w+)', partie)

        if len(sub_parties) > 1:
            # Multiple invités détectés
            for i, sub in enumerate(sub_parties):
                sub = sub.strip()
                if ',' in sub:
                    # Format "Nom, fonction"
                    nom_parts = sub.split(',', 1)
                    nom = nom_parts[0].strip()
                    intitule = nom_parts[1].strip() if len(nom_parts) > 1 else ''
                else:
                    # Pas de virgule, c'est juste un nom
                    nom = sub
                    intitule = ''

                if nom:
                    invites.append({'nom': nom, 'intitule': intitule})
        else:
            # Un seul invité
            if ',' in partie:
                nom_parts = partie.split(',', 1)
                nom = nom_parts[0].strip()
                intitule = nom_parts[1].strip() if len(nom_parts) > 1 else ''
            else:
                nom = partie.strip()
                intitule = ''

            if nom:
                invites.append({'nom': nom, 'intitule': intitule})

    return invites

def parse_matinale_line(text):
    """Parse une ligne de matinale et retourne une liste de dictionnaires (un par invité)"""
    if not text or text.strip() == '':
        return []

    # Pattern pour extraire l'heure
    heure_match = re.match(r'(\d{1,2}h\d{2})', text)
    if not heure_match:
        return []

    heure = heure_match.group(1)

    # Enlever l'heure du début
    reste = text[len(heure):].strip().lstrip('.')

    invites = []

    # Diviser par les chaînes (séparées par ... ou … ou des points de suspension)
    # Pattern pour séparer les chaînes : chaine : nom, intitulé
    chaines_parts = re.split(r'\s*…\s*', reste)

    for part in chaines_parts:
        if not part.strip():
            continue

        # Pattern : Chaine : Nom, intitulé
        match = re.match(r'([^:]+):\s*(.+)', part.strip())
        if match:
            chaine = match.group(1).strip()
            personne_info = match.group(2).strip()

            # Parser les invités multiples
            invites_parsed = parse_invites_multiples(personne_info)

            # Ajouter chaque invité avec la même chaîne et heure
            for invite in invites_parsed:
                invites.append({
                    'heure': heure,
                    'chaine': chaine,
                    'nom': invite['nom'],
                    'intitule': invite['intitule']
                })

    return invites

def main():
    input_file = '/Users/samgoeta/Downloads/Politico/Matinales dans Politico - Feuille 1.csv'
    output_file = '/Users/samgoeta/Downloads/Politico/matinales_formatees.csv'

    resultats = []

    # Lire le CSV d'entrée
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            date = row.get('Date', '')
            texte = row.get('Texte', '')

            if not date or not texte:
                continue

            # Convertir la date au format YYYY-MM-DD
            date_formatee = parse_date(date)

            # Parser la ligne
            invites = parse_matinale_line(texte)

            # Ajouter chaque invité avec la date
            for invite in invites:
                resultats.append({
                    'date_newsletter': date_formatee,
                    'heure': invite['heure'],
                    'chaine': invite['chaine'],
                    'nom_invite': invite['nom'],
                    'intitule_invite': invite['intitule']
                })

    # Écrire le CSV de sortie
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['date_newsletter', 'heure', 'chaine', 'nom_invite', 'intitule_invite']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(resultats)

    print(f"✓ Fichier généré : {output_file}")
    print(f"✓ Nombre d'entrées : {len(resultats)}")

if __name__ == '__main__':
    main()
