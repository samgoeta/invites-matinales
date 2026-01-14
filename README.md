# Extracteur de Matinales Politico

Ce projet contient un script Python pour extraire et formater les informations des matinales politiques depuis les newsletters Politico.

## Contexte

Les newsletters Politico contiennent des sections "matinales" qui listent les interventions d'invités politiques dans différentes émissions de radio et télévision. Ce projet extrait ces informations et les structure dans un format CSV exploitable.

## Fichiers

- **`Matinales dans Politico - Feuille 1.csv`** : Fichier source contenant les newsletters Politico copiées-collées manuellement
  - Format : 2 colonnes (Date, Texte)
  - Date au format DD/MM/YY
  - Texte contenant les informations des matinales

- **`parse_matinales.py`** : Script Python qui parse les données et génère le CSV formaté

- **`matinales_formatees.csv`** : Fichier de sortie généré (621 entrées)
  - Format : CSV avec séparateur virgule, encodage UTF-8
  - Une ligne par invité

- **`test_regex.py`** : Script de test pour valider les expressions régulières

## Format de sortie

Le CSV généré contient les colonnes suivantes :
- **date_newsletter** : Date au format YYYY-MM-DD (ex: 2024-10-09)
- **heure** : Heure de l'émission (ex: 7h40)
- **chaine** : Nom de la chaîne (ex: TF1, RTL, France Inter, etc.)
- **nom_invite** : Nom et prénom de l'invité
- **intitule_invite** : Fonction, titre ou description de l'invité

### Exemple

```csv
date_newsletter,heure,chaine,nom_invite,intitule_invite
2025-12-18,8h20,France Inter,François-Régis Gaudry,"critique gastronomique, auteur de On va déguster Paris"
2025-12-18,8h20,France Inter,Chloé Charles,cheffe cuisinière
2025-12-18,8h20,France Inter,Loïc Bienassis,historien spécialiste de l'alimentation
```

## Fonctionnalités du script

### 1. Conversion de dates
Convertit les dates du format DD/MM/YY vers YYYY-MM-DD

### 2. Extraction des horaires
Détecte automatiquement les horaires au format "7h40", "8h15", etc.

### 3. Séparation des chaînes
Parse les différentes chaînes de télévision/radio séparées par "…" (points de suspension)

### 4. Séparation des invités multiples
Le script gère intelligemment la séparation des invités lorsque plusieurs personnes sont mentionnées :
- Sépare les invités reliés par " et " suivi d'un nom propre complet (Prénom Nom)
- Sépare les invités dans une liste séparée par des virgules
- **Conserve** les "et" dans les titres/fonctions (ex: "ministre de l'Égalité entre les femmes et les hommes")

### 5. Extraction nom/intitulé
- Le nom est avant la première virgule
- L'intitulé est après la première virgule
- Si pas de virgule, tout est considéré comme le nom

## Utilisation

```bash
python3 parse_matinales.py
```

Le script va :
1. Lire le fichier `Matinales dans Politico - Feuille 1.csv`
2. Parser chaque ligne pour extraire les informations
3. Générer `matinales_formatees.csv`
4. Afficher le nombre d'entrées créées

## Cas particuliers gérés

### Invités multiples sur une même chaîne
```
8h20. France Inter : François-Régis Gaudry, critique gastronomique, Chloé Charles, cheffe cuisinière et Loïc Bienassis, historien
```
→ Crée 3 lignes séparées, une pour chaque invité

### Plusieurs chaînes au même horaire
```
7h40. TF1 : Maud Bregeon, députée … RTL : Aurore Bergé, porte-parole … RMC : Thomas Ménagé, porte-parole du RN
```
→ Crée 3 lignes avec la même heure mais des chaînes différentes

### Titres contenant "et"
```
Aurore Bergé, ministre chargée de l'Egalité entre les femmes et les hommes
```
→ Le titre complet est conservé intact dans intitule_invite

### Caractères spéciaux
Le script gère correctement les caractères accentués français (é, è, à, ï, ü, etc.)

## Structure du code

### Fonction `parse_date(date_str)`
Convertit DD/MM/YY en YYYY-MM-DD

### Fonction `parse_invites_multiples(personne_info)`
Parse une chaîne contenant potentiellement plusieurs invités et retourne une liste de dictionnaires {nom, intitule}

Utilise des regex avancées pour :
- Détecter les séparations par " et " suivies d'un nom propre complet
- Détecter les séparations par ", " suivies d'un nom propre complet
- Ne pas diviser les "et" dans les titres/fonctions

### Fonction `parse_matinale_line(text)`
Parse une ligne complète de matinale et retourne une liste d'entrées (une par invité)

### Fonction `main()`
Orchestre le processus complet : lecture, parsing, écriture du CSV

## Statistiques

- **Fichier source** : ~764 lignes (incluant les lignes vides)
- **Fichier généré** : 621 entrées (invités)
- **Période couverte** : Jusqu'à janvier 2026

## Traitement des données

Après extraction, les données ont été enrichies et validées selon le processus suivant :

### Enrichissement avec Wikidata
Les données ont été alignées avec Wikidata dans **OpenRefine** pour récupérer :
- L'âge des invités
- Le genre des invités

### Contrôle qualité manuel
Les données enrichies ont été contrôlées manuellement par une équipe d'étudiants du **M2 Métiers de l'Information (EJCAM et Sciences Po Aix)** dans le cadre du cours de data journalisme et médiation :

- Marion Gastebled
- Mélissandre Delchet
- Lila Besson
- Erica Landon
- Mathieu Belluteau
- Lilou Botta

Ce contrôle manuel a permis de valider et corriger les informations récupérées automatiquement depuis Wikidata.

## Notes techniques

### Patterns regex utilisés

```python
# Détection heure
r'(\d{1,2}h\d{2})'

# Séparation par "…"
r'\s*…\s*'

# Séparation par " et " + nom propre
r'\s+et\s+(?=[A-ZÉÈÀÊÂÔÛÇÏÜ]\w+\s+[A-ZÉÈÀÊÂÔÛÇÏÜ])'

# Séparation par ", " + nom propre complet
r',\s+(?=[A-ZÉÈÀÊÂÔÛÇÏÜ]\w+\s+[A-ZÉÈÀÊÂÔÛÇÏÜ]\w+)'

# Extraction chaîne : invité
r'([^:]+):\s*(.+)'
```

## Améliorations possibles

- Ajouter la détection automatique des nouvelles newsletters
- Créer une interface graphique pour visualiser les données
- Générer des statistiques (invités les plus fréquents, chaînes les plus actives, etc.)
- Ajouter un système de validation des données extraites
- Gérer les cas edge non encore rencontrés

## Prérequis

- Python 3.x
- Modules standards : `csv`, `re`, `datetime`

Aucune dépendance externe nécessaire.

---

## Crédits

Ce code a été généré avec **Claude Code** (Anthropic), un assistant IA pour le développement logiciel.
