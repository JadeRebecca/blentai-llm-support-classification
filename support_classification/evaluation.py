import torch
from sklearn.metrics import f1_score


def normalize_prediction(prediction, valid_labels):
    cleaned_prediction = prediction.strip()

    if cleaned_prediction in valid_labels:
        return cleaned_prediction

    lowered_prediction = cleaned_prediction.lower()
    for label in valid_labels:
        if lowered_prediction == label.lower():
            return label

    for label in valid_labels:
        lowered_label = label.lower()
        if lowered_prediction.startswith(lowered_label) or lowered_label in lowered_prediction:
            return label

    return cleaned_prediction


def predict_queue(prompt, model, tokenizer, valid_labels, max_new_tokens=12):
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {key: value.to(model.device) for key, value in inputs.items()}

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    generated_ids = output_ids[0][inputs["input_ids"].shape[1] :]
    prediction = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    prediction = prediction.split("\n")[0].strip()
    return normalize_prediction(prediction, valid_labels)


def evaluate_model(dataset, model, tokenizer, valid_labels, model_name):
    evaluation_df = dataset.copy()
    evaluation_df["prediction"] = evaluation_df["prompt"].apply(
        lambda prompt: predict_queue(prompt, model, tokenizer, valid_labels)
    )

    weighted_f1 = f1_score(
        evaluation_df["answer"],
        evaluation_df["prediction"],
        average="weighted",
        zero_division=0,
    )

    print(f"{model_name} weighted F1-score: {weighted_f1:.2%}")
    return evaluation_df, weighted_f1
