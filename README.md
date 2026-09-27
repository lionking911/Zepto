# Zepto

Zepto is a modular Python project containing three independent, production-ready modules:

- **Book Scraper & SQLite Analytics** — Web scraping with semantic search and SQL/pandas analysis
- **Titanic Analytics & Machine Learning** — EDA, preprocessing, model comparison, and hyperparameter tuning
- **AI-Powered Support Assistant** — RAG-based customer support using ChromaDB, LangGraph, Groq, and FastAPI

Each module is self-contained with its own dependencies, documentation, and configuration.

## Repository structure

```text
Zepto/
├── README.md                             # This file
├── requirements.txt                      # Root-level dependencies
├── data_pipeline/
│   ├── README.md                         # Book scraper documentation
│   ├── scraper.py                        # Scraper entry point
│   ├── bookscrap.db                      # Generated SQLite database
│   └── scraper_html/                     # Cached HTML pages
├── analytics/
│   ├── EDAREADME.md                      # Exploratory data analysis guide
│   ├── MODELINGREADME.md                 # Model training and evaluation guide
│   ├── eda.py                            # EDA entry point
│   ├── modeling.py                       # Model training entry point
│   ├── titanic.csv                       # Raw dataset
│   ├── cleaned_titanic.csv               # Preprocessed dataset
│   ├── full_prediction_pipeline.joblib   # Trained model artifact
│   └── screenshots/                      # Visualization outputs
└── support_assistant/
    ├── README.md                         # Canonical support assistant documentation
    ├── SUPPORTREADME.md                  # Legacy documentation
    ├── support_assistances.py            # FastAPI application
    ├── requirements.txt                  # Module dependencies
    ├── support_assistant_docker.dockerfile
    ├── data/                             # Policy documents
    │   ├── DeliveryPolicy.txt
    │   ├── ReturnsRefunds.txt
    │   ├── MembershipTiers.txt
    │   ├── OrderTracking.txt
    │   ├── OrderCancellationPolicy.txt
    │   ├── DamagedorMissingItems.txt
    │   ├── GiftCards.txt
    │   └── CustomerSupportHours.txt
    ├── firstdemostration.png
    └── seconddemonstration.png
```

## Module Overview

### 1. Book Scraper & SQLite Analytics

**Location:** `data_pipeline/`

Scrapes book data from [books.toscrape.com](https://books.toscrape.com/), cleans it, stores in SQLite, and performs analytical queries.

**Key features:**

- Web scraping with `requests` and `BeautifulSoup`
- HTML caching for repeat runs without re-downloading
- SQLite database with two tables: `categories` and `product_details`
- Currency conversion: GBP → INR (£1 = ₹105.50)
- SQL and pandas analytics examples: GROUP BY, JOIN, window functions, correlation

**Database schema:**

| Table | Columns |
|---|---|
| `categories` | id, title, link, scraped_at |
| `product_details` | id, title, rating, price_pound, price_inr, availability, categorie_id (FK) |

**Run:**

```bash
python data_pipeline/scraper.py
```

Or from inside the module:

```bash
cd data_pipeline && python scraper.py
```

**Key functions:**

- `fetch_url(url)` — HTTP GET with retry and error handling
- `db_connect(db)` — SQLite connection
- `db_create_table(conn, cursor, query)` — Create tables
- `db_insert_list(conn, cursor, query, data)` — Batch insert
- `db_fetch_all()`, `db_fetch_one()` — Retrieve results

**First run:** Downloads homepage and category pages, creates tables, inserts records.

**Subsequent runs:** Reuses cached HTML and database, runs queries without scraping.

**Error handling:** HTTPError, ConnectionError, Timeout, RequestException, sqlite3.Error.

See [`data_pipeline/README.md`](data_pipeline/README.md) for complete documentation.

---

### 2. Titanic Analytics & Machine Learning

**Location:** `analytics/`

End-to-end workflow for Titanic dataset: EDA, preprocessing, model training, evaluation, and persistence.

#### Exploratory Data Analysis

**File:** `eda.py`

**Outputs:**

- `titanic.csv` — Raw dataset (auto-downloaded if missing)
- `cleaned_titanic.csv` — Preprocessed dataset
- Interactive visualizations

**EDA steps:**

1. **Data loading** — Fetch from Seaborn if local CSV missing
2. **Data inspection** — `.info()`, `.describe()`, unique values per column
3. **Missing value analysis** — Calculate % missing per column; drop/impute based on threshold
4. **Redundancy detection** — Identify duplicate columns (e.g., `alive` vs `survived`)
5. **Duplicate removal** — Drop exact row duplicates
6. **Outlier analysis** — IQR method on `fare` and `age`
7. **Distribution & skewness** — Summary statistics and visualization
8. **Correlation** — Pearson correlation matrix for numeric columns
9. **Feature engineering** — Map categorical labels (e.g., `alive` → 1/0)
10. **Data scaling** — StandardScaler example on `age` and `fare`

**Key findings:**

- **Survival by gender:** Women had significantly higher survival rates (signal)
- **Survival by class:** First and second class passengers survived more often than third class
- **Survival by fare:** Higher fare passengers had better survival odds
- **Distribution:** Age appears approximately normal; fare is right-skewed

**Run:**

```bash
python analytics/eda.py
```

See [`analytics/EDAREADME.md`](analytics/EDAREADME.md) for complete EDA documentation.

#### Machine Learning Modeling

**File:** `modeling.py`

**Workflow:**

1. **Data preparation** — Load `cleaned_titanic.csv`, stratified train/test split (80/20)
2. **Preprocessing** — ColumnTransformer with separate pipelines for numeric (impute + scale) and categorical (impute + one-hot encode) features
3. **Model comparison** — Train and evaluate three classifiers:
   - Logistic Regression
   - Decision Tree (max_depth=5)
   - Random Forest (n_estimators=100, max_depth=6)
4. **Evaluation metrics** — Accuracy, Precision, Recall, F1, ROC-AUC, confusion matrix, ROC curve
5. **Class imbalance handling** — Compare three strategies:
   - Baseline (no balancing)
   - Class weight balanced
   - SMOTE (on training fold only)
6. **Hyperparameter tuning** — GridSearchCV on Random Forest with n_estimators=[1000], max_depth=[5,10,None], max_features=['sqrt','log2']
7. **Regression task** — Predict `fare` using Linear Regression
8. **Model persistence** — Save best pipeline as `full_prediction_pipeline.joblib`

**Model comparison table:**

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC | Recommendation |
|---|---|---|---|---|---|---|
| Logistic Regression | 78.2% | 0.75 | 0.70 | 0.73 | 0.844 | — |
| Decision Tree | 80.1% | 0.85 | 0.63 | 0.72 | 0.847 | — |
| **Random Forest** | **81.4%** | **0.89** | **0.63** | **0.73** | **0.851** | **Best** |

**Recommendation:** Random Forest delivers the highest accuracy and ROC-AUC, making it the most reliable model for distinguishing between survival classes.

**Class imbalance results:**

| Strategy | Precision | Recall | F1 Score |
|---|---|---|---|
| Baseline (no handling) | 0.719 | 0.667 | 0.692 |
| **Class weight balanced** | **0.702** | **0.760** | **0.730** |
| SMOTE (train fold only) | 0.722 | 0.729 | 0.725 |

**Recommendation:** Class weight balanced achieved the highest F1 score and recall, best for this imbalance scenario.

**Regression (fare prediction):**

- MAE: 22.61
- RMSE: 45.65
- R²: 0.353

**Run:**

```bash
python analytics/modeling.py
```

**Model loading:**

```python
import joblib

pipeline = joblib.load("full_prediction_pipeline.joblib")
predictions = pipeline.predict(new_raw_input)
probabilities = pipeline.predict_proba(new_raw_input)[:, 1]
```

**Dependencies:**

```bash
pandas numpy matplotlib seaborn scikit-learn imbalanced-learn tabulate joblib
```

See [`analytics/MODELINGREADME.md`](analytics/MODELINGREADME.md) for complete modeling documentation.

---

### 3. AI-Powered Support Assistant

**Location:** `support_assistant/`

Customer support chatbot using RAG (retrieval-augmented generation) with ChromaDB, LangGraph, Groq LLM, and FastAPI.

**Architecture:**

```text
User query
    ↓
Classify intent (policy_question or general_question)
    ├→ Policy: Retrieve from ChromaDB + Generate answer
    └→ General: Direct LLM answer
    ↓
Return structured response (answer, sources, confidence)
```

**Key features:**

- **Intent classification** — LLM-based or keyword-based (testing mode)
- **Semantic retrieval** — ChromaDB with sentence transformers embeddings
- **Answer generation** — Pydantic-validated JSON with source attribution
- **Workflow orchestration** — LangGraph state machine
- **Automatic retry** — JSON parse errors trigger up to 2 retries
- **REST API** — FastAPI endpoint

**Setup:**

```bash
pip install -r support_assistant/requirements.txt
```

Create `support_assistant/.env`:

```dotenv
GROQ_API_KEY=your_api_key_here
```

**Start the API:**

```bash
uvicorn support_assistant.support_assistances:app --host 127.0.0.1 --port 8050 --reload
```

**API request:**

```bash
curl -X POST "http://127.0.0.1:8050/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "What is the policy for returns?",
    "mock_llm": 1
  }'
```

**API response:**

```json
{
  "query": "What is the policy for returns?",
  "detected_intent": "policy_question",
  "agent_response": "Returns are accepted within 30 days of purchase...",
  "source": ["Returns & Refunds"],
  "confidence": 0.92
}
```

**Programmatic usage:**

```python
from support_assistant.support_assistances import apple

response = apple.invoke({"query": "What is the policy for returns?"})
print(response["intent"])        # policy_question
print(response["answer"])         # Returns are accepted...
print(response["sources"])        # ['Returns & Refunds']
print(response["confidence"])     # 0.92
```

**Policy documents (8 total):**

- Delivery Policy
- Returns & Refunds
- Membership Tiers
- Order Tracking
- Order Cancellation Policy
- Damaged or Missing Items
- Gift Cards
- Customer Support Hours

**Testing mode (mock_llm=1):**

- Uses keyword-based classification
- Returns deterministic responses
- No LLM calls, instant results
- Useful for development and testing

**Production mode (mock_llm=0):**

- Uses Groq LLM for classification
- Context-aware answer generation
- Requires valid GROQ_API_KEY
- Full RAG pipeline

**Configuration:**

```text
ChromaDB path: /content/zepto_knowledge_db
Collection: compnay_docs
Model: qwen/qwen3.8-27b
Retrieval: 3 results
Temperature: 0.0 (deterministic)
Max retries: 2
```

**Docker deployment:**

```bash
docker build -t zepto-support-assistant -f support_assistant/support_assistant_docker.dockerfile .
docker run --rm -p 8050:8050 -e GROQ_API_KEY=your_key zepto-support-assistant
```

**Troubleshooting:**

| Issue | Cause | Solution |
|---|---|---|
| FileNotFoundError | Missing policy files | Check `support_assistant/data/` has all 8 `.txt` files |
| HTTP 422 | Missing API field | Include both `user_query` and `mock_llm` |
| GROQ_API_KEY error | Invalid/missing key | Create `.env` with valid key, restart server |
| No documents retrieved | Empty database or overly specific query | Verify ChromaDB and try simpler query |
| JSON decode error | LLM returned non-JSON | Check logs; automatic retry happens |
| Slow response | LLM latency | Reduce `n_results` or use mock mode |

See [`support_assistant/README.md`](support_assistant/README.md) for comprehensive documentation.

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip or conda
- Internet access (scraper, dataset downloads, Groq API)
- Groq API key (for support assistant production mode)

### Create a virtual environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install module dependencies

**For Book Scraper:**

```bash
pip install requests beautifulsoup4 ftfy pandas tabulate
```

**For Titanic Analytics:**

```bash
pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn tabulate joblib
```

**For Support Assistant:**

```bash
pip install -r support_assistant/requirements.txt
```

**For all modules:**

```bash
pip install -r requirements.txt
```

### Environment variables

Support assistant production mode:

```bash
export GROQ_API_KEY="your_api_key_here"
export DB_PATH="/content/zepto_knowledge_db"
export MODEL_NAME="qwen/qwen3.8-27b"
export MOCK_LLM="0"
```

Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_api_key_here"
$env:DB_PATH="/content/zepto_knowledge_db"
$env:MODEL_NAME="qwen/qwen3.8-27b"
$env:MOCK_LLM="0"
```

---

## Quick Start

### 1. Run the Book Scraper

```bash
python data_pipeline/scraper.py
```

Outputs: `bookscrap.db`, cached HTML in `scraper_html/`.

### 2. Run Titanic EDA

```bash
python analytics/eda.py
```

Outputs: `cleaned_titanic.csv`, visualizations.

### 3. Train Titanic Models

```bash
python analytics/modeling.py
```

Outputs: `full_prediction_pipeline.joblib`, model metrics.

### 4. Start Support Assistant API

```bash
uvicorn support_assistant.support_assistances:app --host 127.0.0.1 --port 8050 --reload
```

Test:

```bash
curl -X POST "http://127.0.0.1:8050/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_query":"What is the return policy?","mock_llm":1}'
```

---

## Module Documentation

- [`data_pipeline/README.md`](data_pipeline/README.md) — Scraper: schema, queries, caching
- [`analytics/EDAREADME.md`](analytics/EDAREADME.md) — EDA: analysis steps, findings
- [`analytics/MODELINGREADME.md`](analytics/MODELINGREADME.md) — ML: training, evaluation, persistence
- [`support_assistant/README.md`](support_assistant/README.md) — Support Assistant: setup, API, configuration, troubleshooting

---

## Project Structure Notes

- Modules are **independent** and can be run separately
- Each module has its own dependencies (`requirements.txt`) and documentation
- Generated artifacts (databases, CSVs, cached files, models) are created during execution
- Do **not** commit `.env` files or secrets to the repository
- The support assistant API must be started with **Uvicorn**; importing the Python file alone does not start the server

---

## Status

Active development on the `devlopment` branch.

**Last updated:** September 2026  
**Maintainer:** Zepto Team
