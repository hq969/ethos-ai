from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

class ComplianceGuardian:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def sanitize_input(self, text: str):
        """
        Scans text for PII (GDPR/HIPAA) and redacts it.
        """
        # Analyze text for PII entities
        results = self.analyzer.analyze(text=text, language='en')
        
        # Define redaction operators (e.g., replace with <REDACTED>)
        operators = {
            "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<PHONE>"}),
            "US_SSN": OperatorConfig("replace", {"new_value": "<SSN>"}),
            "CREDIT_CARD": OperatorConfig("replace", {"new_value": "<CREDIT_CARD>"}),
        }
        
        # Anonymize
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators=operators
        )
        
        return {
            "original_text": text,
            "sanitized_text": anonymized_result.text,
            "entities_detected": [res.entity_type for res in results]
        }

# Example Usage
if __name__ == "__main__":
    guardian = ComplianceGuardian()
    sample = "Patient John Doe with SSN 123-45-6789 requested a loan."
    print(guardian.sanitize_input(sample))
