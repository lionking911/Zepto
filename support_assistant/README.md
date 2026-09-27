# Zepto Support Assistant

An AI-powered customer support assistant for Zepto using retrieval-augmented generation (RAG), ChromaDB, LangGraph, Groq, Pydantic, and FastAPI.

## Overview

The assistant:

- Classifies queries as `policy_question` or `general_question`.
- Retrieves relevant policy content from ChromaDB.
- Generates answers with source attribution and confidence scores.
- Uses LangGraph to route queries through the appropriate workflow.
- Exposes a FastAPI endpoint at `POST /chat`.

Workflow:

```text
User query → Classify intent → Route query
                         ├── Policy question → Retrieve documents → Generate answer
                         └── General question → Direct answer
```

## Project structure

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
├── README.md
├── SUPPORTREADME.md              # Legacy documentation; this README is canonical
├── support_assistances.py
├── requirements.txt
├── support_assistant_docker.dockerfile
├── firstdemostration.png
└── seconddemonstration.png
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

Create `support_assistant/.env` for production LLM mode:

```dotenv
GROQ_API_KEY=your_api_key_here
```

## Running the API

The Python module creates the FastAPI application but does not automatically start a server. Start it with Uvicorn.

From the repository root:

```bash
uvicorn support_assistant.support_assistances:app --host 127.0.0.1 --port 8050 --reload
```

Or from inside `support_assistant/`:

```bash
uvicorn support_assistances:app --host 127.0.0.1 --port 8050 --reload
```

The API is available at `http://127.0.0.1:8050`.

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
| `mock_llm` | integer | Intended to select testing mode (`1`) or LLM mode (`0`). |

The current `QueryRequest` model requires both fields. The current workflow uses the module-level `MOCK_LLM` value, so request-level mode selection should be synchronized with the implementation before relying on it in production.

### Current response format

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

From the repository root:

```python
from support_assistant.support_assistances import apple

response = apple.invoke({"query": "What is the policy for returns?"})

print(response["intent"])
print(response["answer"])
print(response["sources"])
print(response["confidence"])
```

When importing from inside the `support_assistant` directory, use:

```python
from support_assistances import apple
```

## Policy documents

The assistant indexes these eight policy document types:

| Document | Purpose |
|---|---|
| Delivery Policy | Shipping times, regions, and costs |
| Returns & Refunds | Return process and refund timelines |
| Membership Tiers | Benefits, eligibility, and renewal |
| Order Tracking | Tracking status and updates |
| Order Cancellation Policy | Cancellation rules and timelines |
| Damaged or Missing Items | Claims and resolution process |
| Gift Cards | Purchase, usage, and expiry |
| Customer Support Hours | Availability and contact channels |

Documents are loaded from `support_assistant/data/` when the module is imported.

## Output schema

The internal answer model is `AnswerOutput`:

```json
{
  "answer": "string",
  "sources": ["document name"],
  "confidence": 0.0
}
```

- `answer`: The generated response.
- `sources`: Policy documents used for the answer. General questions should return an empty list.
- `confidence`: A score from `0.0` to `1.0`.

## Configuration

Current implementation defaults:

```text
ChromaDB path: /content/zepto_knowledge_db
Collection: compnay_docs
Model: qwen/qwen3.8-27b
Temperature: 0.0
Retrieval results: 3
```

The module loads `GROQ_API_KEY` from `support_assistant/.env`. The documented `DB_PATH`, `MODEL_NAME`, and `MOCK_LLM` environment variables require corresponding `os.getenv()` handling in the Python implementation before they affect runtime behavior.

### ChromaDB

Persistent storage is currently configured as:

```python
chroma_client = chromadb.PersistentClient(
    path="/content/zepto_knowledge_db"
)
collection = chroma_client.get_or_create_collection(
    name="compnay_docs"
)
```

For development, ChromaDB can be changed to an ephemeral client:

```python
chroma_client = chromadb.EphemeralClient()
```

### Mock and production modes

The intended configuration is:

```python
# Testing: keyword classification and deterministic responses
MOCK_LLM = 1

# Production: Groq LLM classification and generation
MOCK_LLM = 0
```

The current source declares `MOCK_LLM` as an integer but compares it with the string `'1'`. Normalize the type before relying on mock mode:

```python
if MOCK_LLM == 1:
    # mock mode
    pass
```

Testing mode recognizes these policy keywords:

```python
[
    "delivery", "return", "refund", "membership",
    "tracking", "cancel", "gift card", "support hours"
]
```

## Retrieval configuration

The default retrieval count is three chunks:

```python
retrieved_docs, retrieved_metadata = retrieve(question, n_results=3)
```

Use more context:

```python
retrieved_docs, retrieved_metadata = retrieve(question, n_results=5)
```

Use fewer results for faster responses:

```python
retrieved_docs, retrieved_metadata = retrieve(question, n_results=1)
```

Document chunks shorter than 50 characters are currently skipped in `chunk_documents()`.

## Error handling

LLM answer-generation and direct-answer flows retry invalid JSON or validation failures up to two times. If all retries fail, the assistant returns an error response with confidence `0.0`.

| Problem | Likely cause | Solution |
|---|---|---|
| `FileNotFoundError` | Missing policy file | Verify all files exist in `support_assistant/data/`. |
| HTTP 422 | Missing API field | Include both `user_query` and `mock_llm`. |
| `GROQ_API_KEY` error | Missing or invalid key | Create `support_assistant/.env` and restart the server. |
| No documents retrieved | Empty database or overly specific query | Check files and try a shorter query. |
| JSON decode error | Model returned non-JSON text | Check logs; the application retries automatically. |
| Model/API error | Invalid model, quota, or network issue | Verify Groq model availability and credentials. |
| Slow responses | LLM latency or excessive retrieval | Reduce `n_results` or use mock mode. |
| High memory usage | Large database or context | Reduce chunk size and retrieval count. |

Check the collection with:

```python
from chromadb import PersistentClient

client = PersistentClient(path="/content/zepto_knowledge_db")
collection = client.get_collection(name="compnay_docs")
print(collection.count())
```

## Docker deployment

Build the image from the repository root:

```bash
docker build \
  -t zepto-support-assistant \
  -f support_assistant/support_assistant_docker.dockerfile .
```

Run it:

```bash
docker run --rm -p 8050:8050 \
  -e GROQ_API_KEY=your_api_key_here \
  zepto-support-assistant
```

## Testing examples

### Policy question

```python
response = apple.invoke({"query": "What is the policy for returns?"})
assert response["intent"] == "policy_question"
```

### General question

```python
response = apple.invoke({"query": "What is the capital of France?"})
assert response["intent"] == "general_question"
```

### Ambiguous policy query

```python
response = apple.invoke({"query": "Tell me about membership"})
assert response["intent"] == "policy_question"
```

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

`asyncio` is part of the Python standard library and does not normally need to be installed with pip. The current Python file also imports `pandas`; add `pandas` to `requirements.txt` if that import remains in use.

## Future enhancements

- [ ] Multi-turn conversation history
- [ ] User feedback loop for confidence calibration
- [ ] Fine-tuned embeddings for the Zepto domain
- [ ] Document versioning and hot updates
- [ ] Analytics dashboard for query patterns
- [ ] Multi-language support
- [ ] Ticket management integration
- [ ] Custom intent categories such as billing and technical support
- [ ] Response personalization based on user tier
- [ ] Rate limiting and authentication
- [ ] Query caching and batch processing

## Support and contribution

For issues or improvements:

1. Check this README and the troubleshooting section.
2. Review application logs.
3. Test with mock mode first.
4. Include the query, expected output, actual output, and relevant logs when filing an issue.

**Canonical documentation:** This `README.md` combines the previous `README.md` and `SUPPORTREADME.md`.  
**Branch:** `devlopment`  
**Maintainer:** Zepto Support Team
