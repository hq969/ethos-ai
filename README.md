# EthosAI: Responsible Generative AI Framework

**EthosAI** is a compliance and safety layer designed for high-stakes Generative AI applications (Finance, Healthcare, Governance). It acts as a middleware between the user and the LLM (Google Gemini Pro), ensuring that all inputs are sanitized for PII and all outputs are audited for bias and toxicity before reaching the end-user.

---

## 🏗️ System Architecture



The system operates on a **Microservices Architecture** with three core guardians:
1.  **The Guardian (Compliance):** Redacts PII (GDPR/HIPAA) using Microsoft Presidio.
2.  **The Auditor (Bias & Safety):** Detects toxicity and bias using Hugging Face transformers.
3.  **The Explainer (Transparency):** Generates visual and textual explanations for AI decisions.

---

## 🚀 Features

* **Real-time PII Redaction:** Automatically detects and masks Credit Cards, SSNs, and Phone Numbers.
* **Bias "Circuit Breaker":** Blocks generated content if it exceeds toxicity thresholds.
* **Multimodal Explainability:** Provides a "Reasoning Trace" and visualization for every response.
* **Adversarial Defense:** Includes a "Red Team" script to test system robustness against jailbreaks.
* **Cloud Native:** Ready for deployment on Google Cloud Run.

---

## 🛠️ Prerequisites

* **Python 3.9+**
* **Google Cloud Platform Account** (with Vertex AI API enabled)
* **Docker** (optional, for containerization)

---

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/ethos-ai.git](https://github.com/your-username/ethos-ai.git)
    cd ethos-ai
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_lg
    ```

4.  **Set Up Google Cloud Credentials**
    * Ensure you have a Service Account Key JSON file.
    * Set the environment variable:
        ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/key.json"
        export PROJECT_ID="your-gcp-project-id"
        ```

---

## 🏃‍♂️ Usage

### 1. Start the API Server
Run the FastAPI gateway. This will initialize the Compliance, Bias, and Explainability engines.
```bash
python main.py

```

*The server will start at `http://0.0.0.0:8080*`

### 2. Manual Testing (cURL)

Open a new terminal and send a request with sensitive data to see the redaction in action:

```bash
curl -X POST "http://localhost:8080/generate_safe" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test_user", "prompt": "My name is John Doe and my SSN is 123-45-6789. Can you confirm my loan status?"}'

```

### 3. Run Adversarial "Red Team" Tests

Run the automated test suite to attempt "jailbreaking" the model and verify that the safety layers hold up.

```bash
python adversarial_test.py

```

---

## 📂 Project Structure

```text
ethos-ai/
├── main.py                   # FastAPI Gateway & Vertex AI Integration
├── compliance_service.py     # PII Redaction (Presidio)
├── bias_engine.py            # Toxicity Detection (Transformers)
├── explainability_engine.py  # Visualization Generation
├── adversarial_test.py       # Red Team Testing Suite
├── requirements.txt          # Python Dependencies
├── Dockerfile                # Container Configuration
└── README.md                 # Project Documentation

```

---

## 🚢 Deployment (Google Cloud Run)

To deploy this framework as a serverless microservice:

```bash
# 1. Build the container
gcloud builds submit --tag gcr.io/$PROJECT_ID/ethos-ai-gateway .

# 2. Deploy to Cloud Run
gcloud run deploy ethos-ai-service \
  --image gcr.io/$PROJECT_ID/ethos-ai-gateway \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

```

---

## 📜 License

MIT License. See `LICENSE` for more information.

---
