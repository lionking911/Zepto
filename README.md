# Zepto

Zepto is a 3-in-1 Python project that brings together:

- Web scraping with a SQLite-backed book catalog
- Titanic data analytics and machine learning
- An AI-powered customer support assistant using RAG and LangGraph

This repository is organized as three independent modules, each with its own scripts, data files, and documentation.

## Repository structure

```text
Zepto/
├── README.md
├── Analytics/
│   ├── EDAREADME.md
│   ├── MODELINGREADME.md
│   ├── cleaned_titanic.csv
│   ├── eda.py
│   ├── full_prediction_pipeline.joblib
│   ├── modeling.py
│   ├── screenshots/
│   └── titanic.csv
├── SupportAssistances/
│   ├── Customer Support Hours
│   ├── Damaged or Missing Items
│   ├── Delivery Policy
│   ├── Gift Cards
│   ├── Membership Tiers
│   ├── Order Cancellation Policy
│   ├── Order Tracking
│   ├── Returns & Refunds
│   ├── SUPPORTREADME.md
│   └── support_assistances.py
├── scraper/
│   ├── README.md
│   ├── scraper.py
│   └── scraped_html/
└── .gitignore
```

## Modules

### 1) Book scraper
Location: `scraper/`

The scraper collects book information from books.toscrape.com, cleans the data, and stores it in SQLite. It also runs SQL and pandas-based analytical queries to inspect pricing, ratings, and category relationships.

Run:

```bash
python scraper/scraper.py
```

### 2) Titanic analytics and ML
Location: `Analytics/`

This section includes:

- Exploratory data analysis (`eda.py`)
- Model training and evaluation (`modeling.py`)
- Titanic datasets (`titanic.csv`, `cleaned_titanic.csv`)
- Trained pipeline artifact (`full_prediction_pipeline.joblib`)

Run:

```bash
python Analytics/eda.py
python Analytics/modeling.py
```

### 3) Support assistant
Location: `SupportAssistances/`

This module builds a customer support assistant using retrieval-augmented generation (RAG), semantic retrieval, and a FastAPI-based chatbot interface. It uses policy documents in the folder to answer support questions with source-aware responses.

Run:

```bash
python SupportAssistances/support_assistances.py
```

Once started, the service can be queried through the API exposed by the script.

## Getting started

### Prerequisites

- Python 3.8+
- pip
- Internet access for the scraper and dataset download flow

### Install dependencies

```bash
pip install requests beautifulsoup4 ftfy pandas numpy scikit-learn imbalanced-learn matplotlib seaborn tabulate joblib chromadb sentence-transformers langgraph pydantic fastapi uvicorn nest-asyncio groq
```

If you are using a virtual environment, create one first:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

## Environment variables

For the support assistant, optional environment values can be configured:

```bash
export GROQ_API_KEY="your_api_key_here"
export DB_PATH="/content/zepto_knowledge_db"
export MODEL_NAME="qwen/qwen3.8-27b"
export MOCK_LLM="0"
```

## Documentation

Each module has its own README and supporting notes:

- `scraper/README.md`
- `Analytics/EDAREADME.md`
- `Analytics/MODELINGREADME.md`
- `SupportAssistances/SUPPORTREADME.md`

## Notes

- The repository is structured as modular, independent components rather than a single app.
- Each module can be run separately.
- Some generated artifacts, such as CSVs, model files, and scraped HTML caches, are created during execution.
- README updates are maintained as the repository evolves.

## Status

Active development.
