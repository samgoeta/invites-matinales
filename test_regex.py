#!/usr/bin/env python3
import re

text = "cheffe cuisinière et Loïc Bienassis, historien spécialiste de l'alimentation"

# Ancien pattern
pattern_old = r'\s+et\s+(?=[A-ZÉÈÀÊÂÔÛÇ][a-zéèàêâôûçœ]+\s+[A-ZÉÈÀÊÂÔÛÇ])'
parts_old = re.split(pattern_old, text)
print('OLD Pattern:')
print('Parts:', parts_old)
print('Length:', len(parts_old))

# Nouveau pattern avec \w pour capturer tous les caractères unicode
pattern_new = r'\s+et\s+(?=[A-ZÉÈÀÊÂÔÛÇÏÜ]\w+\s+[A-ZÉÈÀÊÂÔÛÇÏÜ])'
parts_new = re.split(pattern_new, text)
print('\nNEW Pattern:')
print('Parts:', parts_new)
print('Length:', len(parts_new))
