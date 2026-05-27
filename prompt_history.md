# Historique des prompts

## Prompt v1

Statut :
- Utilise pour les essais precedents du pipeline `SequenceClassification`
- Prompt plus verbeux, avec formulation type assistant

Contenu :

```text
You are a support ticket classification assistant.
Choose exactly one support ticket category from the allowed labels below.
Return only the exact label name and do not add any explanation.

Allowed labels:
- {label_1}
- {label_2}
- ...

Ticket information:
Subject: {subject}
Body: {body}
Language: {language}
Business type: {business_type}

Answer:
```

Commentaire :
- Ce prompt conserve une logique de consigne tres explicite
- Il correspond au prompt de reference retenu dans ce projet
- Le meilleur resultat actuel obtenu avec ce prompt dans le suivi est `weighted F1 = 85.38%` et `macro F1 = 87.16%` sur l'essai 6

## Prompt v2

Statut :
- Teste comme variante plus compacte
- Reference : `Essai 8` dans `results_tracking.md`

Contenu :

```text
Classify the support ticket into one allowed label.

Allowed labels:
- {label_1}
- {label_2}
- ...

Subject: {subject}
Body: {body}
Language: {language}
Business type: {business_type}

Label:
```

Commentaire :
- Ce prompt reduit le texte d'instruction pour donner un signal de classification plus direct
- Il a obtenu `weighted F1 = 83.21%` et `macro F1 = 87.37%` sur l'essai 8
- Il reste moins bon que le prompt v1 sur ce projet
