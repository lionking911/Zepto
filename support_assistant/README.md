# Zepto Support Assistant

An AI-powered customer support assistant for Zepto using retrieval-augmented generation (RAG), ChromaDB, LangGraph, Groq, and FastAPI.

## Project location

This module is located in `support_assistant/`.

```text
support_assistant/
├── data/
│   ├── DeliveryPolicy.txt
│   ├── ReturnsRefunds.txt
│   ├── MembershipTiers.txt
│   ├── OrderTracking.txt
│   ├── OrderCancellationPolicy.txt
│   ├── DamagedorMissingItems.txt
│   ├── GiftCards.txt
│   └── CustomerSupportHours.txt
├── support_assistances.py
├── requirements.txt
├── SUPPORTREADME.md
└── README.md
```

## Installation

From the repository root:

```bash
pip install -r support_assistant/requirements.txt
```

Or from inside the module:

```bash
cd support_assistant
pip install -r requirements.txt
```

Create `support_assistant/.env` and add your Groq API key when using production LLM mode:

```dotenv
GROQ_API_KEY=your_api_key_here
```

## Start the API

From the repository root:

```bash
uvicorn support_assistant.support_assistances:app --host 127.0.0.1 --port 8050 --reload
```

Or from inside `support_assistant/`:

```bash
uvicorn support_assistances:app --host 127.0.0.1 --port 8050 --reload
```

The API is available at `http://127.0.0.1:8050`.

> Running `python support_assistances.py` only imports and builds the application; use Uvicorn to start the server unless a server entry point is added to the script.

## API usage

Send a request to `POST /chat`:

```bash
curl -X POST "http://127.0.0.1:8050/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "What is the policy for returns?",
    "mock_llm": 1
  }'
```

### Request fields

| Field | Type | Description |
|---|---|---|
| `user_query` | string | Customer question. |
| `mock_llm` | integer | Use `1` for deterministic keyword/canned testing mode and `0` for LLM mode. |

### Response

The current implementation returns a response similar to:

```json
{
  "query": "What is the policy for returns?",
  "source": ["Returns & Refunds"],
  "confidence": 0.92,
  "detected_intent": "policy_question",
  "agent_response": "Returns are accepted according to the Returns & Refunds policy."
}
```

`agent_response` is currently a string. `source` contains the document names used to answer the question, and `confidence` is between `0.0` and `1.0`.

## Programmatic usage

```python
from support_assistant.support_assistances import apple

response = apple.invoke({"query": "What is the policy for returns?"})

print(response["intent"])
print(response["answer"])
print(response["sources"])
print(response["confidence"])
```

## How it works

1. The query is classified as `policy_question` or `general_question`.
2. Policy questions retrieve relevant chunks from the ChromaDB collection.
3. The retrieved context is passed to the answer-generation step.
4. General questions are handled by the direct-answer step.
5. The LangGraph workflow returns the answer, sources, intent, and confidence.

The workflow is:

```text
Classify intent → Route query → Retrieve and answer / Direct answer → Return response
```

## Policy documents

The assistant indexes these eight document types:

- Delivery Policy
- Returns & Refunds
- Membership Tiers
- Order Tracking
- Order Cancellation Policy
- Damaged or Missing Items
- Gift Cards
- Customer Support Hours

Documents are loaded from `support_assistant/data/` when the module is imported.

## Configuration

The current script uses the following defaults:

```text
ChromaDB path: /content/zepto_knowledge_db
Collection: compnay_docs
Model: qwen/qwen3.8-27b
Retrieval results: 3
```

The `.env` file is loaded from `support_assistant/.env`. The current code requires `GROQ_API_KEY` when `MOCK_LLM` is disabled. If you customize database path, model, or mock-mode configuration through environment variables, ensure the Python implementation also reads those variables with `os.getenv()`.

## Testing mode

The source currently declares `MOCK_LLM` as an integer and compares it with the string `'1'`. Until that implementation is normalized, use the same type consistently in code. The intended behavior is:

```python
MOCK_LLM = 1

if MOCK_LLM == 1:
    # keyword-based classification and deterministic responses
    pass
```

Testing mode recognizes these keywords:

```python
[
    "delivery", "return", "refund", "membership",
    "tracking", "cancel", "gift card", "support hours"
]
```

## Troubleshooting

### `FileNotFoundError` for policy documents

Run the application from the repository or module using the commands above and verify that all eight `.txt` files exist in `support_assistant/data/`.

### API returns HTTP 422

The current `QueryRequest` model requires both `user_query` and `mock_llm`. Include both fields in the JSON request.

### `GROQ_API_KEY` errors

Create `support_assistant/.env` with a valid key and restart Uvicorn. Use testing mode to avoid LLM calls while developing.

### No documents are retrieved

Check that the policy files are not empty and that the ChromaDB collection has been populated. Try a shorter query such as:

```text
What is the return policy?
```

### Model or API errors

Verify the Groq model name, API key, quota, and network connection. The answer-generation and direct-answer flows retry failed JSON responses up to two times before returning an error response.

## Dependencies

Dependencies are listed in `requirements.txt`:

```text
chromadb
langgraph
pydantic
sentence-transformers
groq
fastapi
uvicorn
python-dotenv
```

`asyncio` is part of the Python standard library and does not normally need to be installed separately. The script also imports `pandas`; add `pandas` to the requirements file if that import remains in use.

## Related documentation

- [`SUPPORTREADME.md`](./SUPPORTREADME.md) — original support assistant documentation
- [`README.md`](../README.md) — repository overview

**Branch:** `devlopment`  
**Maintainer:** Zepto Support Team
