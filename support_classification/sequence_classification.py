import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.metrics import f1_score
from transformers import Trainer


def build_label_mappings(valid_labels):
    label_to_id = {label: index for index, label in enumerate(valid_labels)}
    id_to_label = {index: label for label, index in label_to_id.items()}
    return label_to_id, id_to_label


def encode_classification_dataframe(dataframe, label_to_id):
    encoded_df = dataframe.copy()
    encoded_df["labels"] = encoded_df["answer"].map(label_to_id)
    if encoded_df["labels"].isna().any():
        missing_labels = sorted(encoded_df.loc[encoded_df["labels"].isna(), "answer"].unique())
        raise ValueError(f"Unknown labels found in dataset: {missing_labels}")

    encoded_df["labels"] = encoded_df["labels"].astype(int)
    return encoded_df


def dataframe_to_hf_dataset(dataframe):
    return Dataset.from_pandas(dataframe[["prompt", "labels"]], preserve_index=False)


def tokenize_classification_dataset(dataset, tokenizer, max_length=768):
    def tokenize_batch(batch):
        return tokenizer(
            batch["prompt"],
            truncation=True,
            max_length=max_length,
        )

    return dataset.map(tokenize_batch, batched=True, remove_columns=["prompt"])


def build_class_weights(encoded_labels, num_labels):
    counts = np.bincount(encoded_labels, minlength=num_labels)
    total = counts.sum()
    weights = total / (num_labels * counts)
    return torch.tensor(weights, dtype=torch.float32)


class WeightedClassificationTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.get("logits")

        weight = None
        if self.class_weights is not None:
            weight = self.class_weights.to(logits.device)

        loss_fct = torch.nn.CrossEntropyLoss(weight=weight)
        loss = loss_fct(logits.view(-1, model.config.num_labels), labels.view(-1))

        if return_outputs:
            return loss, outputs
        return loss


def build_compute_metrics(id_to_label):
    def compute_metrics(eval_prediction):
        logits, labels = eval_prediction
        predicted_ids = np.argmax(logits, axis=-1)

        predicted_labels = [id_to_label[int(predicted_id)] for predicted_id in predicted_ids]
        true_labels = [id_to_label[int(label_id)] for label_id in labels]

        weighted_f1 = f1_score(
            true_labels,
            predicted_labels,
            average="weighted",
            zero_division=0,
        )
        macro_f1 = f1_score(
            true_labels,
            predicted_labels,
            average="macro",
            zero_division=0,
        )

        return {
            "weighted_f1": weighted_f1,
            "macro_f1": macro_f1,
        }

    return compute_metrics


def predict_labels(dataframe, model, tokenizer, id_to_label, max_length=768):
    encoded_dataset = tokenize_classification_dataset(
        dataframe_to_hf_dataset(dataframe.assign(labels=0)),
        tokenizer,
        max_length=max_length,
    )

    trainer = Trainer(model=model, processing_class=tokenizer)
    predictions = trainer.predict(encoded_dataset)
    predicted_ids = np.argmax(predictions.predictions, axis=-1)

    prediction_df = dataframe.copy()
    prediction_df["prediction"] = [id_to_label[int(predicted_id)] for predicted_id in predicted_ids]
    return prediction_df


def evaluate_sequence_classifier(dataframe, model, tokenizer, id_to_label, model_name, max_length=768):
    prediction_df = predict_labels(
        dataframe=dataframe,
        model=model,
        tokenizer=tokenizer,
        id_to_label=id_to_label,
        max_length=max_length,
    )

    weighted_f1 = f1_score(
        prediction_df["answer"],
        prediction_df["prediction"],
        average="weighted",
        zero_division=0,
    )
    macro_f1 = f1_score(
        prediction_df["answer"],
        prediction_df["prediction"],
        average="macro",
        zero_division=0,
    )

    print(f"{model_name} weighted F1-score: {weighted_f1:.2%}")
    print(f"{model_name} macro F1-score: {macro_f1:.2%}")
    return prediction_df, weighted_f1, macro_f1


def save_label_mappings(path, valid_labels, label_to_id):
    payload = {
        "labels": valid_labels,
        "label_to_id": label_to_id,
    }
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
