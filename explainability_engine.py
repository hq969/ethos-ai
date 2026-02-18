import matplotlib.pyplot as plt
import io
import base64
import numpy as np

class ExplainabilityEngine:
    def generate_explanation(self, input_text, model_confidence_scores):
        """
        Generates a visual heatmap of factor importance.
        """
        # Mocking feature importance for demonstration
        features = ["Credit_History", "Income_Level", "Debt_Ratio", "Collateral"]
        importance = np.random.rand(4) # In real scenario, use SHAP values here
        
        # Create Visualization
        plt.figure(figsize=(6, 4))
        colors = ['green' if x > 0.5 else 'red' for x in importance]
        plt.barh(features, importance, color=colors)
        plt.title("AI Decision Factor Importance")
        plt.xlabel("Influence Score")
        
        # Save to Base64 string
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        img_b64 = base64.b64encode(img_buf.read()).decode('utf-8')
        plt.close()
        
        # Textual Explanation
        explanation_text = (
            f"The model approved this based primarily on '{features[np.argmax(importance)]}'. "
            "However, debt ratio was a negative influencing factor."
        )

        return {
            "explanation_text": explanation_text,
            "visualization_base64": img_b64
        }
