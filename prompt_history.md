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
- Le meilleur resultat actuel obtenu avec ce prompt dans le suivi est `weighted F1 = 87.54%` et `macro F1 = 93.32%` sur l'essai 13

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

## Prompt v3

Statut :
- Variante ciblee sur les classes techniques les plus souvent confondues
- Teste dans `Essai 14` de `results_tracking.md`

Contenu :

```text
You are a support ticket classification assistant.
Choose exactly one support ticket category from the allowed labels below.
Return only the exact label name and do not add any explanation.

Guidance for close technical labels:
- IT Support: access, accounts, permissions, devices, internal tools or workstation issues.
- Technical Support: bugs, errors, crashes, malfunctions or troubleshooting on the product/service.
- Product Support: how to use, configure or understand product features and workflows.

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
- Ce prompt conserve la structure explicite du prompt v1
- Il ajoute une aide locale uniquement pour les classes techniques qui restent les plus confondues
- Il a obtenu `weighted F1 = 88.99%` et `macro F1 = 91.99%` sur l'essai 14
- Il améliore le `weighted F1` par rapport au prompt v1, mais reste sous la cible de `92%`

## Prompt v4

Statut :
- Variante plus discriminante sur les classes proches observees dans l'analyse d'erreurs
- Prete pour l'essai suivant apres `Essai 14`

Contenu :

```text
You are a support ticket classification assistant.
Choose exactly one support ticket category from the allowed labels below.
Return only the exact label name and do not add any explanation.

Decision guide for close labels:
- Product Support: how to use, configure, understand, or get help with a product or service feature.
- Technical Support: bugs, errors, crashes, malfunctions, troubleshooting, or a product/service not working correctly.
- Customer Service: general customer assistance, orders, returns, exchanges, refunds, account help, or non-technical support requests.
- IT Support: access, accounts, permissions, devices, workstations, internal tools, or internal technical issues.
- Billing and Payments: invoices, charges, refunds, payment methods, billing problems, or account balance issues.

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
- Ce prompt garde la structure explicite des versions precedentes
- Il ajoute une separation plus nette entre les classes encore les plus confondues
- Il cible directement les confusions observees entre `Technical Support`, `Product Support`, `Customer Service`, `IT Support` et `Billing and Payments`
