import unittest

from support_classification.prompts import build_prompt


class BuildPromptTests(unittest.TestCase):
    def test_build_prompt_includes_constraints_labels_and_ticket_fields(self):
        valid_labels = ["Billing", "Customer Service", "Returns and Exchanges"]

        prompt = build_prompt(
            subject="Refund request",
            body="I want to return my last order.",
            language="en",
            business_type="E-commerce",
            valid_labels=valid_labels,
        )

        self.assertIn("Choose exactly one support ticket category", prompt)
        self.assertIn("Return only the exact label name", prompt)
        self.assertIn("Guidance for close technical labels:", prompt)
        self.assertIn("- IT Support: access, accounts, permissions, devices, internal tools or workstation issues.", prompt)
        self.assertIn("- Technical Support: bugs, errors, crashes, malfunctions or troubleshooting on the product/service.", prompt)
        self.assertIn("- Product Support: how to use, configure or understand product features and workflows.", prompt)
        self.assertIn("Allowed labels:\n- Billing\n- Customer Service\n- Returns and Exchanges", prompt)
        self.assertIn("Subject: Refund request", prompt)
        self.assertIn("Body: I want to return my last order.", prompt)
        self.assertIn("Language: en", prompt)
        self.assertIn("Business type: E-commerce", prompt)
        self.assertTrue(prompt.endswith("Answer:"))

    def test_build_prompt_preserves_label_order(self):
        valid_labels = ["Returns and Exchanges", "Billing", "Customer Service"]

        prompt = build_prompt(
            subject="Question",
            body="Need help",
            language="fr",
            business_type="Retail",
            valid_labels=valid_labels,
        )

        labels_block = (
            "Allowed labels:\n"
            "- Returns and Exchanges\n"
            "- Billing\n"
            "- Customer Service"
        )
        self.assertIn(labels_block, prompt)


if __name__ == "__main__":
    unittest.main()
