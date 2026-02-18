from transformers import pipeline
import torch

class BiasDetector:
    def __init__(self):
        # Load a small efficient model for toxicity detection
        self.classifier = pipeline(
            "text-classification", 
            model="unitary/unbiased-toxic-roberta", 
            return_all_scores=True
        )

    def audit_response(self, text: str, threshold=0.7):
        """
        Audits the generated text for bias/toxicity.
        Returns Pass/Fail status and a risk report.
        """
        results = self.classifier(text)[0]
        
        # Extract scores
        risk_report = {res['label']: res['score'] for res in results}
        
        # Check against threshold
        is_safe = True
        flagged_categories = []
        
        for category, score in risk_report.items():
            if score > threshold:
                is_safe = False
                flagged_categories.append(category)
        
        return {
            "is_safe": is_safe,
            "flagged_categories": flagged_categories,
            "risk_scores": risk_report
        }

# Example Usage
if __name__ == "__main__":
    auditor = BiasDetector()
    print(auditor.audit_response("This is a perfectly normal financial report."))
