def build_prompt(subject, body, language, business_type, valid_labels):
    """Build the canonical constrained support-ticket classification prompt."""
    label_lines = "\n".join(f"- {label}" for label in valid_labels)

    return (
        "You are a support ticket classification assistant.\n"
        "Choose exactly one support ticket category from the allowed labels below.\n"
        "Return only the exact label name and do not add any explanation.\n\n"
        "Decision rules:\n"
        "- Product Support: use when the ticket is about how to use, configure, understand, or get help with a product or service feature.\n"
        "- Technical Support: use when the ticket is about bugs, errors, crashes, malfunctions, troubleshooting, or a product/service not working correctly.\n"
        "- IT Support: use when the ticket is about access, accounts, permissions, devices, workstations, internal tools, or internal technical issues.\n"
        "- Customer Service: use when the ticket is about general customer assistance, orders, returns, exchanges, refunds, account help, or non-technical support requests.\n"
        "- Billing and Payments: use when the ticket is about invoices, charges, refunds, payment methods, billing problems, or account balance issues.\n\n"
        "If several labels seem possible:\n"
        "- prefer Technical Support over Product Support when the main issue is a bug or malfunction.\n"
        "- prefer IT Support over Technical Support when the issue is internal access, permissions, or workplace tools.\n"
        "- prefer Billing and Payments over Customer Service when money, charge, invoice, or refund is the main topic.\n\n"
        "Allowed labels:\n"
        f"{label_lines}\n\n"
        "Ticket information:\n"
        f"Subject: {subject}\n"
        f"Body: {body}\n"
        f"Language: {language}\n"
        f"Business type: {business_type}\n\n"
        "Answer:"
    )
