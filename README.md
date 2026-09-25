# Zepto - 3 in 1 Project

A comprehensive Python project combining **Web Scraping**, **Data Analytics & ML**, and **AI-Powered Support Assistant**. This repository showcases end-to-end data engineering, exploratory data analysis, machine learning modeling, and intelligent customer support automation.

## Project Overview

Zepto is a modular project with three independent components:

1. **📚 Book Scraper** - Web scraping with data cleaning and SQL queries
2. **📊 Titanic Analytics** - EDA and predictive modeling on the Titanic dataset  
3. **🤖 Support Assistant** - RAG-based AI customer support system

---

## 🏗️ Project Structure

```
Zepto/
├── README.md                           # Main documentation (this file)
├── main.py                             # Project entry point
├── scraper.py                          # Standalone scraper script
├── pyproject.toml                      # Python project configuration
│
├── scraper/                            # Module 1: Book Scraper
│   ├── README.md                       # Scraper documentation
│   ├── scraper.py                      # Main scraper implementation
│   ├── scraped_html/                   # Cached HTML files (auto-generated)
│   └── bookscrap.db                    # SQLite database (auto-generated)
│
├── Analytics/                          # Module 2: Data Analytics & ML
│   ├── EDAREADME.md                    # Exploratory Data Analysis guide
│   ├── MODELINGREADME.md               # ML Modeling workflow guide
│   ├── eda.py                          # EDA script for Titanic dataset
│   ├── modeling.py                     # ML model training & evaluation
│   ├── titanic.csv                     # Raw dataset
│   ├── cleaned_titanic.csv             # Cleaned dataset
│   └── full_prediction_pipeline.joblib # Trained model artifact
│
├── SupportAssistances/                 # Module 3: AI Support Assistant
│   ├── SUPPORTREADME.md                # Support assistant documentation
│   ├── support_assistances.py          # Main RAG implementation
│   └── zepto_knowledge_db/             # ChromaDB vector store (auto-generated)
│
└── SupportAssistant/                   # Legacy directory
    └── support_assistances.py          # Placeholder
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/lionking911/Zepto.git
cd Zepto

# Install dependencies
pip install -r requirements.txt
# OR install module-specific dependencies (see below)
```

### Running Each Module

#### Module 1: Book Scraper
```bash
python scraper.py
```
Scrapes books.toscrape.com, cleans data, stores in SQLite, and runs analytical queries.

#### Module 2: Titanic Analytics
```bash
# Run EDA
python Analytics/eda.py

# Run Modeling
python Analytics/modeling.py
```
Performs exploratory analysis and trains ML models on the Titanic dataset.

#### Module 3: Support Assistant
```bash
python SupportAssistances/support_assistances.py
```
Starts the FastAPI server on `http://127.0.0.1:8050` for the support assistant chatbot.

---

## 📚 Module Details

### 1. Book Scraper (`scraper/`)

**Purpose**: Extract, clean, and analyze book data from an online bookstore.

**Features**:
- Scrapes book titles, ratings, prices (GBP), and availability
- Cleans and converts data types (prices to float, ratings to int, availability to boolean)
- Converts GBP to INR using fixed rate (1 GBP = 105.50 INR)
- Stores data in normalized SQLite schema with 2-table PK/FK relationship
- Executes 6+ SQL queries demonstrating JOINs, WHERE, ORDER BY, GROUP BY
- Reproduces results using pandas DataFrames and merge operations

**Key Technologies**:
- `requests` - HTTP requests
- `BeautifulSoup4` - HTML parsing
- `sqlite3` - Database operations
- `pandas` - Data analysis
- `tabulate` - Table formatting

**Output**:
- `bookscrap.db` - SQLite database
- Formatted query results printed to console

**Learn More**: See [`scraper/README.md`](scraper/README.md)

---

### 2. Titanic Analytics (`Analytics/`)

This module is split into two workflows:

#### 2a. Exploratory Data Analysis (EDA)
**File**: `Analytics/eda.py`

Performs comprehensive exploratory analysis:
- Loads Titanic dataset from Seaborn
- Inspects data structure, types, and missing values
- Cleans dataset (handles missing data, removes duplicates, drops redundant columns)
- Detects outliers using IQR method
- Analyzes distributions and skewness
- Visualizes patterns (histograms, box plots, heatmaps, survival plots)
- Generates correlation matrix and key insights

**Key Technologies**:
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `seaborn` - Statistical visualization
- `matplotlib` - Plotting
- `scikit-learn` - Preprocessing and scaling

**Output**:
- `titanic.csv` - Raw dataset
- `cleaned_titanic.csv` - Cleaned dataset
- Visual plots and console summaries

**Learn More**: See [`Analytics/EDAREADME.md`](Analytics/EDAREADME.md)

#### 2b. Machine Learning Modeling
**File**: `Analytics/modeling.py`

Builds and compares multiple ML models:
- **Models**: Logistic Regression, Decision Tree, Random Forest
- **Techniques**: Class balancing (SMOTE), hyperparameter tuning (GridSearchCV)
- **Evaluation**: Accuracy, Precision, Recall, F1, ROC-AUC, confusion matrices
- **Tasks**: 
  - Classification: Predicting survival (binary)
  - Regression: Predicting fare prices (continuous)
- **Pipeline**: Full end-to-end preprocessing + model pipeline saved as `.joblib`

**Key Technologies**:
- `scikit-learn` - ML algorithms and preprocessing
- `imbalanced-learn` - SMOTE for class imbalance
- `joblib` - Model serialization
- `tabulate` - Results tables

**Output**:
- `full_prediction_pipeline.joblib` - Trained model
- Comparison tables and ROC curves
- Evaluation metrics and residual plots

**Learn More**: See [`Analytics/MODELINGREADME.md`](Analytics/MODELINGREADME.md)

---

### 3. Support Assistant (`SupportAssistances/`)

**Purpose**: AI-powered customer support using Retrieval-Augmented Generation (RAG).

**Features**:
- **Intent Classification**: Detects policy vs. general questions
- **Semantic Retrieval**: Finds relevant policy documents using ChromaDB
- **Answer Generation**: LLM-based responses with source attribution
- **Confidence Scoring**: 0.0-1.0 confidence per answer
- **REST API**: FastAPI endpoint for integration
- **LangGraph Orchestration**: Robust workflow state management

**Architecture**:
```
User Query
    ↓
Classify Intent (Policy/General)
    ↓
Route to Handler
    ├─ Policy: Retrieve docs + Generate answer
    └─ General: Direct LLM response
    ↓
Return Structured Response {answer, sources, confidence}
```

**Policy Documents Indexed**:
- Delivery Policy
- Returns & Refunds
- Membership Tiers
- Order Tracking
- Order Cancellation
- Damaged or Missing Items
- Gift Cards
- Customer Support Hours

**API Usage**:
```bash
# Start server
python SupportAssistances/support_assistances.py

# Query via curl
curl -X POST "http://127.0.0.1:8050/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_query": "What is the policy for returns?"}'
```

**Key Technologies**:
- `ChromaDB` - Vector database for semantic search
- `sentence-transformers` - Embedding models
- `LangGraph` - Workflow orchestration
- `Pydantic` - Data validation
- `FastAPI` - REST API
- `Groq API` - LLM backend

**Learn More**: See [`SupportAssistances/SUPPORTREADME.md`](SupportAssistances/SUPPORTREADME.md)

---

## 📋 Dependencies

### Core Requirements

```
# Web Scraping
requests
beautifulsoup4
ftfy

# Data Processing
pandas
numpy
scikit-learn
imbalanced-learn

# Visualization
matplotlib
seaborn

# Database
sqlite3 (built-in)

# Utilities
tabulate
joblib

# Support Assistant
chromadb
sentence-transformers
langgraph
pydantic
fastapi
uvicorn
nest-asyncio
groq

# Serialization
joblib
```

### Install All Dependencies

```bash
pip install requests beautifulsoup4 ftfy pandas numpy scikit-learn \
    imbalanced-learn matplotlib seaborn tabulate joblib chromadb \
    sentence-transformers langgraph pydantic fastapi uvicorn \
    nest-asyncio groq
```

Or use pyproject.toml:
```bash
pip install -e .
```

---

## 🔧 Configuration

### Environment Variables (Optional)

For the Support Assistant, set these variables:

```bash
export GROQ_API_KEY="your_api_key_here"
export DB_PATH="/content/zepto_knowledge_db"
export MODEL_NAME="qwen/qwen3.8-27b"
export MOCK_LLM="0"  # 0 = production, 1 = testing mode
```

### Data Paths

Update file paths in each script as needed:

- **Scraper**: HTML cache in `scraper/scraped_html/`
- **Analytics**: Datasets in `Analytics/` directory
- **Support**: Documents in `SupportAssistances/` directory

---

## 📊 Module Outputs & Artifacts

| Module | Key Outputs |
|--------|-----------|
| **Scraper** | `bookscrap.db`, formatted query tables |
| **EDA** | `cleaned_titanic.csv`, visualizations, statistics |
| **Modeling** | `full_prediction_pipeline.joblib`, metrics tables, plots |
| **Support** | ChromaDB index, REST API responses |

---

## 🧪 Testing & Validation

### Book Scraper Validation
- ✅ Scrapes ≥ 60 books across ≥ 3 categories
- ✅ Properly typed columns: `price_gbp`, `rating` (int 1-5), `in_stock` (bool), `price_inr`
- ✅ SQLite schema with 2-table PK/FK relationship
- ✅ ≥ 5 SQL queries with JOINs
- ✅ Pandas merge matches SQL JOIN results

### Titanic EDA Validation
- ✅ Dataset loads successfully
- ✅ Missing values identified and handled
- ✅ Outliers detected using IQR method
- ✅ Visualizations generated (distributions, correlations, survival patterns)
- ✅ Key findings documented

### Titanic Modeling Validation
- ✅ 3+ models trained and compared
- ✅ Classification metrics (accuracy, precision, recall, F1, AUC)
- ✅ Class imbalance handled (SMOTE, class weights)
- ✅ Hyperparameter tuning executed
- ✅ Full pipeline saved and loadable

### Support Assistant Validation
- ✅ Intent classification works
- ✅ Documents retrieved correctly
- ✅ Answers generated with confidence scores
- ✅ REST API responsive
- ✅ Error handling and retries functional

---

## 🚀 Deployment

### Local Development

```bash
cd Zepto
python scraper.py      # Run scraper
python Analytics/eda.py         # Run EDA
python Analytics/modeling.py    # Run modeling
python SupportAssistances/support_assistances.py  # Start API
```

### Docker Deployment

```dockerfile
FROM python:3.9

WORKDIR /app
COPY pyproject.toml .
RUN pip install -e .

COPY . .

# For scraper
CMD ["python", "scraper.py"]

# For analytics
CMD ["python", "Analytics/eda.py"]

# For support assistant
CMD ["python", "SupportAssistances/support_assistances.py"]
```

### Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🐛 Troubleshooting

### Scraper Issues
- **No books scraped**: Check internet connection and website availability
- **Database errors**: Delete `bookscrap.db` and run again
- **Encoding errors**: Ensure UTF-8 encoding support

### Analytics Issues
- **Dataset not found**: Run script with internet connection to download from Seaborn
- **Plot display issues**: On headless servers, use `matplotlib.use('Agg')`
- **Memory issues**: Reduce dataset size or increase available RAM

### Support Assistant Issues
- **No documents retrieved**: Verify policy files exist at specified paths
- **JSON decode error**: Enable `MOCK_LLM='1'` for testing
- **API timeout**: Check Groq API quota and network latency
- **Database errors**: Reinitialize ChromaDB with `chromadb.PersistentClient()`

---

## 📝 Development Notes

### Code Organization
- Each module is independent and can be run separately
- Shared utilities could be extracted to a common `utils/` module
- Consider refactoring for production use (modular functions, CLI, testing)

### Future Improvements
- [ ] Unit tests for each module
- [ ] CLI interface for batch operations
- [ ] Logging framework for production monitoring
- [ ] Configuration management (config.yaml)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] API authentication for Support Assistant
- [ ] Real-time data streaming for Scraper
- [ ] Model versioning and registry
- [ ] Multi-language support for Support Assistant
- [ ] Dashboard for analytics visualization

### Contributing

To contribute improvements:
1. Create a feature branch
2. Make your changes
3. Add tests if applicable
4. Submit a pull request

---

## 📄 License

This project is open source. See individual module documentation for specific license information.

---

## 👤 Author & Maintainer

**lionking911** - GitHub User

---

## 📧 Support & Contact

For issues, questions, or suggestions:
1. Check module-specific README files
2. Review troubleshooting sections
3. File an issue on GitHub
4. Contact the maintainer

---

## 📚 Additional Resources

- [Book Scraper Details](scraper/README.md)
- [Titanic EDA Guide](Analytics/EDAREADME.md)
- [ML Modeling Workflow](Analytics/MODELINGREADME.md)
- [Support Assistant Guide](SupportAssistances/SUPPORTREADME.md)

---

**Last Updated**: September 2026  
**Version**: 1.0  
**Status**: Active Development
