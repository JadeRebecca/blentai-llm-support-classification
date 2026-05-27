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
- Personalized classifier weighted F1-score = 87.49%
- Personalized classifier macro F1-score = 91.75%
- Base classifier weighted F1-score = a mesurer apres rerun de la nouvelle cellule de baseline
- Base classifier macro F1-score = a mesurer apres rerun de la nouvelle cellule de baseline
- Cible 0.92 atteinte = Non sur le weighted F1 connu a ce stade

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
