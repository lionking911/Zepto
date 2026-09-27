# Zepto

Zepto is a modular Python project containing three independent modules:

- **Book Scraper & SQLite Analytics** — Scrapes books from [books.toscrape.com](https://books.toscrape.com/), stores data in SQLite, and runs SQL/pandas analysis.
- **Titanic Analytics & Machine Learning** — Performs EDA, preprocessing, model comparison, hyperparameter tuning, and model persistence.
- **AI-Powered Support Assistant** — Uses RAG, ChromaDB, LangGraph, Groq, and FastAPI to answer Zepto policy questions.

## Repository structure

```text
Zepto/
├── README.md
├── requirements.txt
├── data_pipeline/
│   ├── README.md
│   ├── scraper.py
│   ├── bookscrap.db              # Generated
│   └── scraper_html/             # Generated cache
├── analytics/
│   ├── EDAREADME.md
│   ├── MODELINGREADME.md
│   ├── eda.py
│   ├── modeling.py
│   ├── titanic.csv
│   ├── cleaned_titanic.csv
│   ├── full_prediction_pipeline.joblib
│   └── screenshots/
└── support_assistant/
    ├── README.md
    ├── SUPPORTREADME.md
    ├── requirements.txt
    ├── support_assistances.py
    ├── support_assistant_docker.dockerfile
    └── data/
        ├── DeliveryPolicy.txt
        ├── ReturnsRefunds.txt
        ├── MembershipTiers.txt
        ├── OrderTracking.txt
        ├── OrderCancellationPolicy.txt
        ├── DamagedorMissingItems.txt
        ├── GiftCards.txt
        └── CustomerSupportHours.txt
```

## Quick start

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate      # Windows
```

### Install dependencies

Install the dependencies for the module you need:

```bash
pip install -r requirements.txt
pip install -r support_assistant/requirements.txt
```

## Book scraper

The scraper uses `requests`, `BeautifulSoup`, `ftfy`, pandas, SQLite, and tabulate. It caches HTML pages and creates a `bookscrap.db` database containing `categories` and `product_details` tables.

```bash
python data_pipeline/scraper.py
```

See [`data_pipeline/README.md`](data_pipeline/README.md) for the database schema, key functions, query examples, caching behavior, and error handling.

## Titanic analytics and machine learning

### Exploratory data analysis

The EDA workflow loads or downloads the Titanic dataset, inspects missing values and categorical fields, removes duplicates, handles missing values, detects outliers with the IQR method, analyzes skewness, creates visualizations, calculates correlations, and writes `cleaned_titanic.csv`.

```bash
python analytics/eda.py
```

See [`analytics/EDAREADME.md`](analytics/EDAREADME.md).

### Model training

The modeling workflow uses a `ColumnTransformer` for numeric and categorical preprocessing and compares Logistic Regression, Decision Tree, and Random Forest classifiers. It evaluates accuracy, precision, recall, F1, ROC-AUC, confusion matrices, and ROC curves. It also demonstrates class weighting, SMOTE, GridSearchCV, Linear Regression for fare prediction, and joblib persistence.

The documented baseline results identify Random Forest as the strongest classifier, with approximately 81.4% accuracy and 0.851 ROC-AUC. Class-weight balancing provides the strongest minority-class recall/F1 trade-off in the documented comparison.

```bash
python analytics/modeling.py
```

The trained pipeline is saved as `analytics/full_prediction_pipeline.joblib`.

See [`analytics/MODELINGREADME.md`](analytics/MODELINGREADME.md).

## AI support assistant

The support assistant classifies questions as `policy_question` or `general_question`, retrieves policy chunks from ChromaDB, generates structured answers, and exposes a FastAPI endpoint.

### Install and configure

```bash
pip install -r support_assistant/requirements.txt
```

For production LLM mode, create `support_assistant/.env`:

```dotenv
GROQ_API_KEY=your_api_key_here
```

### Start the API

From the repository root:

```bash
uvicorn support_assistant.support_assistances:app --host 127.0.0.1 --port 8050 --reload
```

The API is available at `http://127.0.0.1:8050`.

### Send a request

```bash
curl -X POST "http://127.0.0.1:8050/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "What is the policy for returns?",
    "mock_llm": 1
  }'
```

The API currently expects both `user_query` and `mock_llm`. Use `mock_llm: 1` for deterministic keyword-based testing and `mock_llm: 0` for LLM mode. The implementation currently uses a module-level `MOCK_LLM` value, so request-level mode selection should be synchronized with the code before relying on it in production.

Example response:

```json
{
  "query": "What is the policy for returns?",
  "source": ["Returns & Refunds"],
  "confidence": 0.92,
  "detected_intent": "policy_question",
  "agent_response": "Returns are accepted according to the Returns & Refunds policy."
}
```

The eight policy documents are loaded from `support_assistant/data/`. ChromaDB uses the configured collection `compnay_docs` and retrieves three chunks by default. LLM failures are retried up to two times when JSON parsing or validation fails.

See [`support_assistant/README.md`](support_assistant/README.md) for complete setup, API, configuration, testing, Docker, and troubleshooting documentation.

## Module documentation

- [`data_pipeline/README.md`](data_pipeline/README.md) — scraper, SQLite schema, queries, and caching
- [`analytics/EDAREADME.md`](analytics/EDAREADME.md) — Titanic EDA and findings
- [`analytics/MODELINGREADME.md`](analytics/MODELINGREADME.md) — training, evaluation, tuning, and persistence
- [`support_assistant/README.md`](support_assistant/README.md) — support assistant setup and API

## Notes

- Run each module independently from the repository root.
- Generated databases, CSVs, cached HTML, plots, and model artifacts may be created during execution.
- Do not commit `.env` files, API keys, or other secrets.
- The support assistant API must be started with Uvicorn; importing the Python module alone does not start the server.

## Status

Active development.
