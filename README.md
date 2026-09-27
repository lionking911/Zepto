# Zepto

Zepto is a modular Python project containing:

- A web scraper with SQLite-backed book catalog analytics
- Titanic exploratory data analysis and machine learning workflows
- An AI-powered customer support assistant using RAG, ChromaDB, LangGraph, Groq, and FastAPI

Each module can be installed, run, and documented independently.

## Repository structure

```text
Zepto/
├── README.md
├── analytics/
│   ├── EDAREADME.md
│   ├── MODELINGREADME.md
│   ├── cleaned_titanic.csv
│   ├── eda.py
│   ├── full_prediction_pipeline.joblib
│   ├── modeling.py
│   ├── screenshots/
│   └── titanic.csv
├── data_pipeline/
│   ├── README.md
│   ├── scraper.py
│   └── scraper_html/
├── support_assistant/
│   ├── data/
│   │   ├── DeliveryPolicy.txt
│   │   ├── ReturnsRefunds.txt
│   │   ├── MembershipTiers.txt
│   │   ├── OrderTracking.txt
│   │   ├── OrderCancellationPolicy.txt
│   │   ├── DamagedorMissingItems.txt
│   │   ├── GiftCards.txt
│   │   └── CustomerSupportHours.txt
│   ├── README.md
│   ├── SUPPORTREADME.md
│   ├── requirements.txt
│   ├── support_assistances.py
│   └── support_assistant_docker.dockerfile
├── requirements.txt
└── .gitignore
```

## Modules

### 1. Book scraper and data pipeline

Location: `data_pipeline/`

The scraper collects book information from [books.toscrape.com](https://books.toscrape.com/), cleans the data, stores it in SQLite, and runs SQL and pandas-based analytics.

Run from the repository root:

```bash
python data_pipeline/scraper.py
```

Or run from inside the module:

```bash
cd data_pipeline
python scraper.py
```

See [`data_pipeline/README.md`](data_pipeline/README.md) for database schema, query examples, caching behavior, and troubleshooting.

### 2. Titanic analytics and machine learning

Location: `analytics/`

This module includes:

- Exploratory data analysis in `eda.py`
- Model training and evaluation in `modeling.py`
- Titanic datasets
- A trained prediction pipeline artifact

Run:

```bash
python analytics/eda.py
python analytics/modeling.py
```

Documentation:

- [`analytics/EDAREADME.md`](analytics/EDAREADME.md)
- [`analytics/MODELINGREADME.md`](analytics/MODELINGREADME.md)

### 3. Support assistant

Location: `support_assistant/`

The support assistant uses policy documents and retrieval-augmented generation to answer Zepto customer-support questions. It provides:

- Intent classification: `policy_question` or `general_question`
- Semantic retrieval from ChromaDB
- LangGraph workflow orchestration
- Groq-based LLM answer generation
- Pydantic output validation
- FastAPI endpoint at `POST /chat`
- Source attribution and confidence scores

Install its dependencies:

```bash
pip install -r support_assistant/requirements.txt
```

Start the API from the repository root:

```bash
uvicorn support_assistant.support_assistances:app --host 127.0.0.1 --port 8050 --reload
```

The API will be available at `http://127.0.0.1:8050`.

Send a request:

```bash
curl -X POST "http://127.0.0.1:8050/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "What is the policy for returns?",
    "mock_llm": 1
  }'
```

The support assistant loads its policy documents from `support_assistant/data/`. For production LLM mode, create `support_assistant/.env`:

```dotenv
GROQ_API_KEY=your_api_key_here
```

See [`support_assistant/README.md`](support_assistant/README.md) for complete setup, API examples, configuration, testing, Docker deployment, and troubleshooting instructions.

## Getting started

### Prerequisites

- Python 3.8+
- pip
- Internet access for the book scraper and Groq API usage
- A Groq API key for support-assistant production mode

### Create a virtual environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install dependencies

Install dependencies for the module you want to use:

```bash
pip install -r support_assistant/requirements.txt
```

For the complete project environment, install the root requirements file as well:

```bash
pip install -r requirements.txt
```

## Support assistant environment variables

The support assistant uses the following configuration values where supported by the implementation:

```bash
export GROQ_API_KEY="your_api_key_here"
export DB_PATH="/content/zepto_knowledge_db"
export MODEL_NAME="qwen/qwen3.8-27b"
export MOCK_LLM="0"
```

On Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_api_key_here"
$env:DB_PATH="/content/zepto_knowledge_db"
$env:MODEL_NAME="qwen/qwen3.8-27b"
$env:MOCK_LLM="0"
```

The support assistant documentation notes that database path, model, and mock-mode environment variables must be read by the Python implementation with `os.getenv()` to affect runtime behavior.

## Documentation

- [`data_pipeline/README.md`](data_pipeline/README.md) — scraper and SQLite analytics
- [`analytics/EDAREADME.md`](analytics/EDAREADME.md) — exploratory data analysis
- [`analytics/MODELINGREADME.md`](analytics/MODELINGREADME.md) — machine learning pipeline
- [`support_assistant/README.md`](support_assistant/README.md) — canonical support assistant documentation
- [`support_assistant/SUPPORTREADME.md`](support_assistant/SUPPORTREADME.md) — legacy support assistant documentation

## Notes

- Modules are independent and can be run separately.
- Generated artifacts such as SQLite databases, cached HTML, CSV files, and model files may be created during execution.
- Do not commit secrets such as `.env` files or API keys.
- The support assistant API should be started with Uvicorn; importing `support_assistances.py` creates the FastAPI app but does not itself start the server.

## Project status

Active development on the `devlopment` branch.
