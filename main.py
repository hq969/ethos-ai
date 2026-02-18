import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

# Import our custom modules
from compliance_service import ComplianceGuardian
from bias_engine import BiasDetector
from explainability_engine import ExplainabilityEngine

app = FastAPI(title="EthosAI Gateway - Gemini Integrated")

# Initialize Google Cloud Project
PROJECT_ID = "your-google-cloud-project-id"  # REPLACE THIS
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Load Gemini Pro
model = GenerativeModel("gemini-1.5-pro-001")

# Initialize Local Microservices
guardian = ComplianceGuardian()
auditor = BiasDetector()
explainer = ExplainabilityEngine()

class PromptRequest(BaseModel):
    user_id: str
    prompt: str

@app.post("/generate_safe")
async def generate_response(request: PromptRequest):
    # Step 1: Compliance Check (Input Redaction)
    print(f"Incoming Request: {request.prompt}")
    sanitized_data = guardian.sanitize_input(request.prompt)
    clean_prompt = sanitized_data["sanitized_text"]
    
    # Step 2: Generate with Gemini Pro
    # We use basic safety settings here, but rely on our internal Auditor for strictness
    try:
        response = model.generate_content(
            clean_prompt,
            safety_settings={
                SafetySetting.Category.HARM_CATEGORY_HATE_SPEECH: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                SafetySetting.Category.HARM_CATEGORY_DANGEROUS_CONTENT: SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }
        )
        generated_content = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Generation Failed: {str(e)}")

    # Step 3: Bias & Safety Audit (The "Circuit Breaker")
    # This checks the LLM's output before the user sees it
    audit_result = auditor.audit_response(generated_content)
    
    if not audit_result["is_safe"]:
        # Log the violation for review but block the response
        print(f"BLOCKED: {audit_result['flagged_categories']}")
        raise HTTPException(
            status_code=400, 
            detail="Response blocked by EthosAI Safety Layer due to policy violation."
        )
    
    # Step 4: Generate Explanations
    explanation = explainer.generate_explanation(clean_prompt, audit_result["risk_scores"])
    
    return {
        "status": "success",
        "original_prompt_redacted": clean_prompt,
        "pii_detected": sanitized_data["entities_detected"],
        "generated_response": generated_content,
        "safety_audit": audit_result,
        "explainability": explanation
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
