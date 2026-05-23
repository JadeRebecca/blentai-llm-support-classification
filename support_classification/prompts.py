def build_prompt(subject, body, language, business_type, valid_labels):
    """Build the canonical constrained support-ticket classification prompt."""
    label_lines = "\n".join(f"- {label}" for label in valid_labels)

    return (
        "You are a support ticket classification assistant.\n"
        "Choose exactly one support ticket category from the allowed labels below.\n"
        "Return only the exact label name and do not add any explanation.\n\n"
        "Allowed labels:\n"
        f"{label_lines}\n\n"
        "Ticket information:\n"
        f"Subject: {subject}\n"
        f"Body: {body}\n"
        f"Language: {language}\n"
        f"Business type: {business_type}\n\n"
        "Answer:"
    )
