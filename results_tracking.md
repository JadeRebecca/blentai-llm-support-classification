Suivi des expériences

Objectif :
Atteindre un weighted F1-score de 0.92 sur le jeu de test.

Modèle de base :
Qwen/Qwen2.5-1.5B-Instruct

Taille des données :
Le notebook indique un train set modeste avec 479 exemples.

Paramètres partagés :
Méthode = SFT + LoRA
Adapter output dir = artifacts/qwen25-support-lora
dataset_text_field = text
max_length = 768
packing = False
num_train_epochs = 4
per_device_train_batch_size = 4
gradient_accumulation_steps = 4
learning_rate = 2e-4
lr_scheduler_type = cosine
warmup_steps = 10
weight_decay = 0.01
logging_steps = 10
save_strategy = epoch
save_total_limit = 2
report_to = none
gradient_checkpointing = True
remove_unused_columns = False
dataloader_pin_memory = False
bf16 = activé si GPU compatible
fp16 = activé sur CUDA si bf16 indisponible
Sinon exécution en float32

Configuration LoRA :
task_type = CAUSAL_LM
r = 16
lora_alpha = 32
lora_dropout = 0.05
bias = none
target_modules = q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj

Configuration d'inférence / évaluation :
Mode = eval()
Génération = greedy decoding
max_new_tokens = 12
do_sample = False
temperature = None
pad_token = eos_token si absent
Normalisation des prédictions = oui, via mapping vers les labels valides
Jeu d'évaluation = test_dataset
Métrique = weighted F1-score

Tableau des essais :

| Essai | Date | Changement principal | Base model | Personalized model | Amélioration | Cible 0.92 atteinte |
|---|---|---|---:|---:|---:|---|
| 1 | 2026-05-23 | Prompt initial sans liste fermée de labels | 17.37% | 50.42% | +33.05 pts | Non |
| 2 | 2026-05-23 | Prompt contraint avec liste fermée de labels via `data/processed/labels.json` | 12.00% | 52.95% | +40.96 pts | Non |

Essai 3 :
Date = 2026-05-27
Changement principal = passage a un classifieur supervise `AutoModelForSequenceClassification` avec LoRA et loss ponderee
Resultats observes dans le notebook actuel :
- Configuration = `use_class_weights = True`
- `learning_rate = 2e-4`
- `num_train_epochs = 6`
- `weight_decay = 0.01`
- Base classifier weighted F1-score = 2.30%
- Base classifier macro F1-score = 2.26%
- Personalized classifier weighted F1-score = 76.69%
- Personalized classifier macro F1-score = 82.91%
- Cible 0.92 atteinte = Non
Conclusion :
- Cette version sert de configuration de reference pour comparer les essais suivants.
- Elle constitue le point de comparaison courant dans ce suivi.

Essai 4 :
Date = 2026-05-27
Changement principal = desactivation de la loss ponderee pour tester une optimisation plus directe du `weighted F1`
Resultats observes dans le notebook actuel :
- Configuration = `use_class_weights = False`
- Base classifier weighted F1-score = 2.30%
- Base classifier macro F1-score = 2.26%
- Personalized classifier weighted F1-score = 82.34%
- Personalized classifier macro F1-score = 85.50%
- Ecart vs essai 3 = +5.65 pts en weighted F1 et +2.59 pts en macro F1 pour le personalized classifier
- Cible 0.92 atteinte = Non
Conclusion :
- La suppression des `class_weights` ameliore ce run par rapport a l'essai 3 propre, mais reste loin de la cible 92%.
- Cette comparaison sert a mesurer l'impact de la loss non ponderee par rapport a la configuration de reference.

Essai 5 :
Date = 2026-05-27
Changement principal = retour a la loss ponderee avec reduction du learning rate pour stabiliser l'apprentissage
Resultats observes dans le notebook actuel :
- `use_class_weights = True`
- `learning_rate = 1e-4`
- Base classifier weighted F1-score = 2.30%
- Base classifier macro F1-score = 2.26%
- Personalized classifier weighted F1-score = 77.21%
- Personalized classifier macro F1-score = 84.56%
- Ecart vs essai 3 = +0.52 pts en weighted F1 et +1.65 pts en macro F1 pour le personalized classifier
- Cible 0.92 atteinte = Non
Conclusion :
- Baisser le `learning_rate` a `1e-4` ne donne pas de gain clair par rapport a la reference propre.
- Le resultat reste proche de la reference, sans amelioration significative.

Essai 6 :
Date = 2026-05-27
Changement principal = retour a la meilleure configuration connue avec augmentation du nombre d'epoques
Resultats observes dans le notebook actuel :
- `use_class_weights = True`
- `learning_rate = 2e-4`
- `num_train_epochs = 8`
- Base classifier weighted F1-score = 2.30%
- Base classifier macro F1-score = 2.26%
- Personalized classifier weighted F1-score = 85.38%
- Personalized classifier macro F1-score = 87.16%
- Ecart vs essai 3 = +8.69 pts en weighted F1 et +4.25 pts en macro F1 pour le personalized classifier
- Cible 0.92 atteinte = Non
Conclusion :
- Passer de 6 a 8 epoques ameliore nettement le score par rapport a l'essai 3 propre.
- Cet essai devient meilleur que l'essai 3 sur le protocole actuel.

Essai 7 :
Date = 2026-05-27
Changement principal = test d'une regularisation plus faible a partir de la meilleure configuration connue
Resultats observes dans le notebook actuel :
- `use_class_weights = True`
- `learning_rate = 2e-4`
- `num_train_epochs = 6`
- `weight_decay = 0.0`
- Base classifier weighted F1-score = 2.30%
- Base classifier macro F1-score = 2.26%
- Personalized classifier weighted F1-score = 81.29%
- Personalized classifier macro F1-score = 89.31%
- Ecart vs essai 3 = +4.60 pts en weighted F1 et +6.40 pts en macro F1 pour le personalized classifier
- Cible 0.92 atteinte = Non
Conclusion :
- Supprimer la regularisation (`weight_decay = 0.0`) ameliore le score par rapport a l'essai 3 propre.
- Cette piste reste interessante dans le protocole actuel, meme si elle n'atteint pas les meilleurs scores observes ensuite.

Essai 8 :
Date = 2026-05-27
Changement principal = test d'un prompt plus compact a partir de la meilleure configuration connue
Resultats observes dans le notebook actuel :
- `use_class_weights = True`
- `learning_rate = 2e-4`
- `num_train_epochs = 6`
- `weight_decay = 0.01`
- prompt actif = version compacte dans `support_classification/prompts.py`
- prompt precedent archive dans `prompt_history.md`
- Base classifier weighted F1-score = 2.30%
- Base classifier macro F1-score = 2.26%
- Personalized classifier weighted F1-score = 83.21%
- Personalized classifier macro F1-score = 87.37%
- Ecart vs essai 3 = +6.52 pts en weighted F1 et +4.46 pts en macro F1 pour le personalized classifier
- Cible 0.92 atteinte = Non
Conclusion :
- Le prompt plus compact fait mieux que l'essai 3 propre, mais reste moins bon que l'essai 6.
- Dans ce suivi, le prompt compact ne devient pas la meilleure option observee.

Essai 9 :
Date = 2026-05-27
Changement principal = nouveau test du prompt compact avec 8 epoques pour verifier si un apprentissage plus long compense la simplification du prompt
Resultats observes dans le notebook actuel :
- `use_class_weights = True`
- `learning_rate = 2e-4`
- `num_train_epochs = 8`
- `weight_decay = 0.01`
- prompt actif = version compacte dans `support_classification/prompts.py`
- Base classifier weighted F1-score = 2.30%
- Base classifier macro F1-score = 2.26%
- Personalized classifier weighted F1-score = 81.06%
- Personalized classifier macro F1-score = 87.10%
- Ecart vs essai 6 = -4.32 pts en weighted F1 et -0.06 pts en macro F1 pour le personalized classifier
- Cible 0.92 atteinte = Non
Conclusion :
- Le prompt compact avec 8 epoques reste moins bon que l'essai 6.
- La piste prompt peut etre consideree comme epuisee a ce stade ; le prochain levier pertinent est le changement de modele.

Pourquoi changer de modele a ce stade :
- Les essais 3 a 9 ont teste plusieurs reglages autour du meme backbone `Qwen/Qwen2.5-1.5B-Instruct` : ponderation de la loss, learning rate, nombre d'epoques, regularisation et variantes de prompt.
- Ces ajustements ont permis de mieux comprendre le comportement du pipeline, mais le meilleur `weighted F1` observe dans ce cadre reste `85.38%` a l'essai 6, encore loin de la cible `92%`.
- L'idee est donc de cesser les micro-ajustements sur un modele qui semble proche de son plafond dans cette configuration, et de tester un backbone plus puissant.
- Un modele open-weight plus puissant reste conforme a la specification et peut mieux separer des classes proches.
- Le cout attendu est plus eleve en temps et en memoire, mais ce changement est maintenant le levier le plus credible pour essayer de gagner plusieurs points de `weighted F1`.

Essai 10 :
Date = 2026-05-27
Changement principal = changement de modele de base en conservant la meilleure configuration actuelle
Resultats observes dans le notebook actuel :
- `base_model_id = backbone plus puissant que Qwen/Qwen2.5-1.5B-Instruct`
- prompt actif = prompt `v1` explicite
- `use_class_weights = True`
- `learning_rate = 2e-4`
- `num_train_epochs = 8`
- `weight_decay = 0.01`
- Base classifier weighted F1-score = 2.30%
- Base classifier macro F1-score = 2.26%
- Personalized classifier weighted F1-score = 86.67%
- Personalized classifier macro F1-score = 92.45%
- Ecart vs essai 6 = +1.29 pts en weighted F1 et +5.29 pts en macro F1 pour le personalized classifier
- Cible 0.92 atteinte = Non
Conclusion :
- Le changement de modele ameliore le meilleur score observe jusqu'ici.
- Le gain reste insuffisant pour atteindre `92%` en `weighted F1`, mais confirme que la capacite du backbone etait bien un levier pertinent.

Pourquoi passer maintenant a l'analyse d'erreurs :
- Apres plusieurs essais d'hyperparametres et un changement de modele, le score continue de progresser mais reste sous la cible.
- Le `macro F1` est deja eleve (`92.45%`), alors que le `weighted F1` reste plus bas (`86.67%`), ce qui suggere que certaines classes frequentes tirent encore la performance vers le bas.
- Avant de lancer un nouvel essai, il devient plus utile d'identifier les confusions les plus couteuses entre classes que de modifier un parametre supplementaire a l'aveugle.
- La prochaine etape est donc d'inspecter la matrice de confusion, le detail par classe et quelques exemples mal classes pour choisir un changement plus cible.

Incident technique avant l'essai suivant :
- Un nouveau backbone plus puissant a ete envisage pour un nouvel essai, mais il n'est pas reconnu correctement par `AutoModelForSequenceClassification` dans l'environnement actuel.
- L'erreur indique une incompatibilite entre sa configuration et le pipeline supervise utilise dans ce notebook.
- Cet essai n'est donc pas comptabilise comme resultat exploitable dans le suivi.
- Il vaut mieux ecarter ce candidat du suivi plutot que de conserver un resultat potentiellement non fiable.

Pourquoi ecarter ce candidat :
- L'objectif reste de tester un backbone plus puissant que `Qwen/Qwen2.5-1.5B-Instruct`.
- Mais un backbone plus fort n'est utile que s'il est charge proprement par le pipeline supervise.
- Quand le chargement produit des avertissements de type de configuration, le resultat peut devenir difficile a interpreter.
- Il est donc plus rigoureux de retirer ce candidat du suivi et de chercher un autre modele clairement compatible.

Essai 11 :
Date = 2026-05-27
Changement principal = tentative de nouveau changement de modele de base
Statut :
- Essai non exploitable en l'etat pour cause d'incompatibilite technique

Configuration testee :
- `base_model_id = backbone plus puissant que Qwen/Qwen2.5-1.5B-Instruct`
- prompt actif = prompt `v1` explicite
- `use_class_weights = True`
- `learning_rate = 2e-4`
- `num_train_epochs = 8`
- `weight_decay = 0.01`
Observation :
- Le chargement du modele produit un avertissement de compatibilite entre le type du modele et la classe auto utilisee.
- Cela indique une incompatibilite entre le modele, la classe auto utilisee et la version actuelle de `transformers`.

Conclusion :
- Cet essai n'est pas retenu pour comparer les performances, car le comportement du pipeline peut etre non fiable.
- Le notebook est remis sur la configuration stable de l'essai 6 en attendant un autre candidat clairement compatible ou une analyse d'erreurs plus poussee.

Pourquoi tester maintenant `Qwen/Qwen2.5-7B-Instruct` :
- Le modele de reference `Qwen/Qwen2.5-1.5B-Instruct` a permis d'obtenir des progres reels, mais semble plafonner sous la cible `92%`.
- Changer de famille de modele a introduit des ambiguïtés techniques, ce qui complique l'interpretation des resultats.
- `Qwen/Qwen2.5-7B-Instruct` permet au contraire d'augmenter la capacite du backbone tout en restant dans une famille deja utilisee avec succes dans ce pipeline.
- L'idee est donc de tester un modele plus grand, mais avec un risque de compatibilite plus faible que les candidats precedemment ecartees.

Essai 12 :
Date = 2026-05-27
Changement principal = passage a un modele plus grand de la meme famille pour tester un gain de capacite avec un risque de compatibilite plus faible
Statut :
- Essai non exploitable en l'etat pour cause de probleme de placement memoire entre CPU et GPU

Configuration testee :
- `base_model_id = 'Qwen/Qwen2.5-7B-Instruct'`
- prompt actif = prompt `v1` explicite
- `use_class_weights = True`
- `learning_rate = 2e-4`
- `num_train_epochs = 8`
- `weight_decay = 0.01`
- historique du modele = `model_history.md`
Observation :
- Le chargement du modele s'effectue, mais l'evaluation echoue avec une erreur indiquant que certains tenseurs sont sur `cuda:0` et d'autres sur `cpu`.
- Cela signifie que le modele est trop lourd ou trop fragmente pour ce mode de chargement dans l'environnement courant.

Conclusion :
- Cet essai n'est pas retenu pour comparer les performances, car il ne produit pas d'evaluation exploitable.
- Le prochain candidat doit rester dans la meme famille, mais avec une taille plus raisonnable.

Pourquoi tester maintenant `Qwen/Qwen2.5-3B-Instruct` :
- L'objectif reste d'augmenter la capacite du backbone par rapport a `Qwen/Qwen2.5-1.5B-Instruct`.
- Le test en `7B` a montre une limite pratique de l'environnement actuel, independante de la qualite theorique du modele.
- `Qwen/Qwen2.5-3B-Instruct` conserve l'avantage d'une famille deja compatible avec le pipeline.
- Il offre plus de capacite que le modele de reference, avec un risque memoire plus faible que la variante `7B`.

Essai 13 :
Date = 2026-05-27
Changement principal = passage a un modele intermediaire de la meme famille pour tester un gain de capacite avec un cout memoire plus raisonnable
Resultats observes dans le notebook actuel :
- `base_model_id = 'Qwen/Qwen2.5-3B-Instruct'`
- prompt actif = prompt `v1` explicite
- `use_class_weights = True`
- `learning_rate = 2e-4`
- `num_train_epochs = 8`
- `weight_decay = 0.01`
- historique du modele = `model_history.md`
- Base classifier weighted F1-score = 3.29%
- Base classifier macro F1-score = 2.08%
- Personalized classifier weighted F1-score = 87.54%
- Personalized classifier macro F1-score = 93.32%
- Ecart vs essai 10 = +0.87 pts en weighted F1 et +0.87 pts en macro F1 pour le personalized classifier
- Cible 0.92 atteinte = Non
Conclusion :
- Cet essai devient le meilleur resultat observe jusqu'ici.
- Le gain est reel mais encore insuffisant pour atteindre `92%` en `weighted F1`.

Ce que montre l'analyse d'erreurs :
- Les principales erreurs concernent les classes techniques les plus frequentes, surtout `Product Support` vs `Technical Support`, puis `Technical Support` vs `IT Support`.
- Ces confusions expliquent bien pourquoi le `macro F1` est deja tres haut alors que le `weighted F1` reste sous la cible : ce sont des classes a fort support qui coutent cher en score pondere.
- Les autres classes sont tres bien separees, souvent avec des rappels et precisions parfaits.
- La prochaine amelioration doit donc cibler ces frontieres de decision entre classes techniques proches, plutot qu'un changement global de configuration.

Pourquoi tester maintenant un prompt guide sur les classes techniques :
- L'analyse d'erreurs montre que les pertes de `weighted F1` viennent surtout de confusions entre `Product Support`, `Technical Support` et `IT Support`.
- Le reste des classes est deja bien separé, donc un changement global de configuration risque d'avoir moins d'effet qu'une aide locale sur ces frontieres de decision.
- L'idee est donc de garder la meilleure base actuelle et d'ajouter dans le prompt une courte clarification semantique pour ces trois labels.
- Cet essai reste peu couteux a lancer et cible directement le principal point faible observe.

Essai 14 :
Date = 2026-05-27
Changement principal = ajout d'une guidance explicite dans le prompt pour reduire les confusions entre classes techniques proches
Configuration preparee pour le prochain run :
- `base_model_id = 'Qwen/Qwen2.5-3B-Instruct'`
- prompt actif = prompt `v3` avec guidance sur `IT Support`, `Technical Support` et `Product Support`
- `use_class_weights = True`
- `learning_rate = 2e-4`
- `num_train_epochs = 8`
- `weight_decay = 0.01`
- historique du prompt = `prompt_history.md`
Resultats :
- A completer apres execution du notebook
Conclusion attendue :
- Cet essai verifie si une clarification locale des classes techniques suffit a gagner les derniers points sur le `weighted F1`.
- S'il n'apporte pas de gain net, il faudra privilegier soit un travail sur les donnees, soit une analyse d'erreurs encore plus fine.

Note :
Le notebook `llm-support-training.ipynb` contient maintenant une cellule supplementaire pour mesurer explicitement le `Base classifier` avant le `Personalized classifier`, ce qui remet une comparaison directe dans la version sequence classification.
Le notebook permet maintenant de basculer facilement entre loss ponderee (`use_class_weights = True`) et loss non ponderee (`use_class_weights = False`) pour mesurer l'impact sur le `weighted F1`.

Lecture rapide :
L'essai 2 est meilleur que l'essai 1 sur le modèle personnalisé : 52.95% contre 50.42%.
La contrainte de sortie semble surtout aider après fine-tuning, car le score du modèle de base baisse de 17.37% à 12.00%.
Les deux essais restent très loin de la cible 92%.

Contrôle qualitatif initial :
résultat obtenus : 2/3

Commentaire :
Ce n'est pas un bug. Le contrôle porte seulement sur 3 exemples du train, donc il n'a pas de valeur statistique forte.
Le 2e ticket est ambigu : son contenu peut faire penser à "Customer Service", même si le label attendu dans le dataset est "Returns and Exchanges".
En plus, "Customer Service" est plus fréquent que "Returns and Exchanges" dans les données d'entraînement, ce qui peut biaiser ponctuellement la génération.

Exemples :
You are a support ticket classification assistant.\nPredict the ticket category from the information below.\n\nSubje..  ans = Product Support pred = Product Support pred
You are a support ticket classification assistant.\nPredict the ticket category from the information below.\n\nSubje.   ans =  Returns and Exchanges	pred = Customer Service
You are a support ticket classification assistant.\nPredict the ticket category from the information below.\n\nSubje..  ans =  Returns and Exchanges	pred = Returns and Exchanges
