def build_prompt(subject, body, language, business_type):
    """Build the canonical support-ticket classification prompt."""
    return (
        "You are a support ticket classification assistant.\n"
        "Predict the ticket category from the information below.\n\n"
        f"Subject: {subject}\n"
        f"Body: {body}\n"
        f"Language: {language}\n"
        f"Business type: {business_type}\n\n"
        "Answer:"
    )
