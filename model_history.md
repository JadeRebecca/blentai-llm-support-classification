# Historique des modèles

## Modèle v1

Nom :
- `Qwen/Qwen2.5-1.5B-Instruct`

Statut :
- Modèle de base de référence pour le pipeline `SequenceClassification`

Pourquoi ce choix :
- Modèle open-weight compatible avec le notebook actuel
- Taille raisonnable pour itérer plus vite sur un dataset modeste
- Support multilingue adapté au projet

Résultats marquants :
- Meilleur résultat observé avec ce modèle : `weighted F1 = 85.38%` et `macro F1 = 87.16%` sur l'essai 6

Commentaire :
- Ce modèle a servi de base à la majorité des essais d'hyperparamètres et de prompt
- Il reste la référence stable du projet

## Modèle v2

Nom :
- Backbone plus puissant testé dans les essais 10 et 11

Statut :
- Testé puis retiré du pipeline

Pourquoi ce choix :
- Chercher un gain de capacité après plusieurs essais de réglages sur le modèle de base de référence

Résultats marquants :
- Un essai a donné `weighted F1 = 86.67%` et `macro F1 = 92.45%`
- Un autre a déclenché un avertissement d'incompatibilité de chargement

Commentaire :
- Comme le chargement est devenu techniquement ambigu dans l'environnement courant, cette piste a été écartée du suivi principal
- Les résultats associés doivent être interprétés avec prudence

## Modèle v3

Nom :
- `Qwen/Qwen2.5-7B-Instruct`

Statut :
- Testé puis écarté dans l'environnement actuel

Pourquoi ce choix :
- Même famille que le modèle de référence, donc compatibilité plus probable avec le pipeline actuel
- Plus grande capacité que `Qwen/Qwen2.5-1.5B-Instruct`
- Bon compromis entre continuité technique et potentiel de gain

Commentaire :
- Le chargement et l'évaluation ont finalement rencontré un problème de placement CPU/GPU dans l'environnement courant
- Ce modèle est donc écarté pour des raisons pratiques, pas parce que le choix était incohérent en soi

## Modèle v4

Nom :
- `Qwen/Qwen2.5-3B-Instruct`

Statut :
- Préparé pour le prochain essai

Pourquoi ce choix :
- Même famille que `Qwen/Qwen2.5-1.5B-Instruct`, donc compatibilité plus probable
- Plus grande capacité que le modèle de référence
- Taille plus raisonnable que `Qwen/Qwen2.5-7B-Instruct` dans l'environnement actuel

Résultats marquants :
- Meilleur résultat observé jusqu'ici : `weighted F1 = 87.54%` et `macro F1 = 93.32%` sur l'essai 13

Commentaire :
- Ce modèle devient la meilleure base actuelle du projet
- Les erreurs restantes se concentrent surtout sur les confusions entre `Product Support`, `Technical Support` et `IT Support`
