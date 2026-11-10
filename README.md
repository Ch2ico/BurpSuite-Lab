# BurpSuite-Lab

Scripts Python et notes d'analyse écrits pendant les exercices de la PortSwigger Web Security Academy, avec Burp Suite.

Chaque dossier d'exercice contient `analysis.txt` (la vulnérabilité, les étapes, les payloads) et, pour la plupart, un script Python qui automatise l'attaque avec `requests` (certains avec `BeautifulSoup`). Les requêtes passent par le proxy Burp Suite (127.0.0.1:8080).

## Contenu

| Série | Exercices | Techniques |
| --- | --- | --- |
| SQLi | 07 à 14 | UNION sur Oracle et MySQL, injection aveugle (cookie, erreur conditionnelle), injection basée sur le temps |
| SSRF | 01 à 04 | serveur local, autre système interne, contournement de liste noire et de liste blanche |
| Authentication_vulnerabilities | 01 à 06 | énumération de comptes (réponses différentes, temps de réponse, verrouillage), contournement de protection anti brute force |

## Utilisation

La plupart des scripts prennent l'URL du laboratoire en argument (`python script.py <url>`), lue via `sys.argv`. À n'utiliser que sur les laboratoires PortSwigger Academy.

## Limites

Exercices de 2023, niveau apprentissage. Plusieurs payloads ne fonctionnent que dans le Repeater de Burp (indiqué dans `analysis.txt`).
