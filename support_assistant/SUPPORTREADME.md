# Zepto Support Assistant

An AI-powered customer support assistant for Zepto that uses retrieval-augmented generation (RAG) and LangGraph to answer customer queries about policies, orders, and services.

## Quick Start

```bash
# Install dependencies
pip install chromadb sentence-transformers langgraph pydantic fastapi uvicorn nest-asyncio

# Run the support assistant
python support_assistances.py
```

## Overview

This module implements an intelligent support system that:
- **Classifies queries** into policy-related or general questions
- **Retrieves relevant documentation** using semantic search (ChromaDB)
- **Generates accurate answers** with source attribution and confidence scores
- **Routes queries** intelligently to appropriate handlers
- **Exposes REST API** via FastAPI for production integration

## Features

### 1. Intent Classification
- Classifies incoming queries as `policy_question` or `general_question`
- Uses LLM-based classification (production) or keyword heuristics (testing)
- Enables intelligent routing to appropriate answer handlers

### 2. Semantic Search & Retrieval
- Stores policy documents in ChromaDB vector database
- Retrieves relevant document chunks using sentence embeddings
- Configurable retrieval (default: top 3 results)
- Supports document versioning and updates

### 3. Answer Generation
- **Policy questions**: Context-based answers from retrieved documents
- **General questions**: Direct LLM-generated responses (policy scope boundary)
- Structured JSON output with Pydantic validation
- Confidence scores (0.0-1.0) based on answer certainty
- Source attribution for traceability

### 4. Workflow Orchestration
- Built with LangGraph for robust state management
- Clear pipeline: Classify → Route → Answer
- Automatic retry logic for LLM failures
- Fallback handling for edge cases

## Architecture

```
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ 1. CLASSIFY INTENT                      │
│ ├─ Keyword matching (MOCK mode)         │
│ └─ LLM classification (production)      │
└────────┬────────────────────────────────┘
         │
    ┌────┴─────────┐
    │              │
    ▼              ▼
┌──────────┐  ┌──────────────┐
│ POLICY   │  │ GENERAL      │
│ QUESTION │  │ QUESTION     │
└────┬─────┘  └────┬─────────┘
     │             │
     ▼             ▼
┌──────────────┐ ┌────────────┐
│ RETRIEVE &   │ │ DIRECT     │
│ ANSWER       │ │ ANSWER     │
│ (with docs)  │ │ (no docs)  │
└────┬─────────┘ └────┬───────┘
     │                │
     └────┬───────────┘
          ▼
┌──────────────────────────────────────┐
│ RETURN STRUCTURED RESPONSE           │
│ {                                    │
│   "answer": "...",                   │
│   "sources": [...],                  │
│   "confidence": 0.85                 │
│ }                                    │
└──────────────────────────────────────┘
```

## Setup & Configuration

### Prerequisites

```bash
pip install chromadb sentence-transformers langgraph pydantic fastapi uvicorn nest-asyncio
```

### Document Configuration

Update file paths in the script to point to your policy documents:

```python
with open("/path/to/Delivery Policy", "r") as f:
    Delivery_Policy = f.read()
with open("/path/to/Returns & Refunds", "r") as f:
    Return_Refunds = f.read()
# ... (add all 8 documents)
```

### Database Configuration

```python
# ChromaDB settings
chroma_client = chromadb.PersistentClient(path="/content/zepto_knowledge_db")
collection = chroma_client.get_or_create_collection(name="compnay_docs")
```

### LLM Model Configuration

```python
# Current model configuration
model = "qwen/qwen3.8-27b"
temperature = 0.0  # Deterministic responses
```

### Testing vs. Production

```python
# Testing mode (keyword-based classification)
MOCK_LLM = '1'

# Production mode (LLM-based)
MOCK_LLM = '0'
```

## Policy Documents

The system indexes 8 policy document types:

| Document | Purpose |
|----------|---------|
| Delivery Policy | Shipping times, regions, costs |
| Returns & Refunds | Return process, refund timelines |
| Membership Tiers | Benefits, eligibility, renewal |
| Order Tracking | Tracking status, updates |
| Order Cancellation Policy | Cancellation rules, timeline |
| Damaged or Missing Items | Claims process, resolution |
| Gift Cards | Purchase, usage, expiry |
| Customer Support Hours | Availability, contact channels |

## Usage

### Programmatic Usage

```python
from support_assistances import apple

# Query the assistant
policy_query = "What is the policy for returns?"
inputs = {"query": policy_query}
response = apple.invoke(inputs)

# Access response
print(f"Answer: {response['answer']}")
print(f"Sources: {response['sources']}")
print(f"Confidence: {response['confidence']}")
```

### API Endpoint

#### Start the Server

```bash
# In the script, the FastAPI server starts automatically on port 8050
# Or manually:
uvicorn support_assistances:appp --host 127.0.0.1 --port 8050
```

#### Make a Request

```bash
curl -X POST "http://127.0.0.1:8050/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "What is the policy for returns?"
  }'
```

#### Response Format

```json
{
  "detected_intent": "policy_question",
  "agent_response": {
    "answer": "Returns are accepted within 30 days of purchase...",
    "sources": ["Returns & Refunds"],
    "confidence": 0.92
  }
}
```

## Output Schema

All responses follow the `AnswerOutput` Pydantic model:

```json
{
  "answer": "string (max 3 sentences for policy questions)",
  "sources": ["list of document names used"],
  "confidence": "float between 0.0 and 1.0"
}
```

### Field Descriptions

- **answer**: Direct, concise answer to the user's query
  - Policy questions: Extracted from retrieved documents
  - General questions: LLM-generated (may redirect to policy scope)
  
- **sources**: List of policy document names used
  - Policy questions: Names of retrieved documents
  - General questions: Empty list (no retrieval)
  
- **confidence**: Certainty score for the answer
  - 1.0: Exact match in documents / clear policy
  - 0.7-0.9: Partial match / inferred from context
  - 0.0: Error state / unable to answer

## Classification Keywords

The system recognizes policy questions using these keywords:

```python
keywords = [
    "delivery",
    "return", 
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours"
]
```

Add custom keywords for your use case:

```python
keywords.extend(["exchange", "warranty", "discount"])
```

## Retrieval Configuration

### Adjust Number of Results

```python
# Default: top 3 results
retrieved_docs, retrieved_metadata = retrieve(question, n_results=3)

# For more context
retrieved_docs, retrieved_metadata = retrieve(question, n_results=5)

# For faster responses
retrieved_docs, retrieved_metadata = retrieve(question, n_results=1)
```

### Chunk Size Tuning

```python
# In chunk_documents() function
if len(para) < 50:  # Minimum chunk size
    continue
```

## Error Handling & Retry Logic

The system includes automatic retry logic for LLM failures:

```python
max_retries = 2  # Number of retry attempts
retries = 0

# On JSON decode error:
# 1. Send corrective instruction to LLM
# 2. Request valid JSON output
# 3. Retry up to max_retries times
# 4. Return error response if all retries fail
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| JSON decode error | LLM response not valid JSON | Automatic retry (up to 2×) |
| Pydantic validation error | Schema mismatch | Check LLM prompt template |
| No documents retrieved | Query too specific | Use shorter queries |
| API timeout | LLM server slow | Increase timeout, check quota |
| Database not found | Wrong path or corrupted | Reinitialize ChromaDB |

## Performance Optimization

### Vector Database

```python
# Persistent storage (recommended for production)
chroma_client = chromadb.PersistentClient(
    path="/content/zepto_knowledge_db"
)

# In-memory (faster for development)
chroma_client = chromadb.EphemeralClient()
```

### Retrieval Speed

- **Chunk size**: Smaller chunks = faster retrieval but less context
- **n_results**: Fewer results = faster but less comprehensive
- **Index type**: Default is HNSW (fast approximate search)

### LLM Response Time

- **Temperature**: 0.0 (deterministic) is faster than > 0.0
- **Batch processing**: Use async API for multiple queries
- **Caching**: Cache frequent queries at application level

## Deployment

### Local Development

```bash
python support_assistances.py
# Server: http://127.0.0.1:8050
```

### Docker Deployment

```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY support_assistances.py .
CMD ["python", "support_assistances.py"]
```

### Production with Public URL

```bash
# Using LocalTunnel
npm install -g localtunnel
npx localtunnel --port 8050
# Generates: https://xyz-abc-123.loca.lt
```

### Environment Variables

```python
# Add to your deployment config
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_PATH = os.getenv("DB_PATH", "/content/zepto_knowledge_db")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen/qwen3.8-27b")
MOCK_LLM = os.getenv("MOCK_LLM", "0")
```

## Testing

### Test Cases

```python
# Policy question
policy_query = "What is the policy for returns?"
inputs = {"query": policy_query}
response = apple.invoke(inputs)
assert response["intent"] == "policy_question"

# General question
general_query = "What is the capital of France?"
inputs = {"query": general_query}
response = apple.invoke(inputs)
assert response["intent"] == "general_question"

# Edge case: ambiguous query
ambiguous_query = "Tell me about membership"
inputs = {"query": ambiguous_query}
response = apple.invoke(inputs)
# Should classify as policy_question
```

### Running Tests

```bash
# Enable debug logging
# Uncomment print() statements in functions

# Test with MOCK_LLM = '1' first
MOCK_LLM = '1'
# Then switch to production
MOCK_LLM = '0'
```

## Troubleshooting

### Issue: "No documents retrieved"

**Symptoms**: Empty retrieved_docs list

**Solutions**:
1. Verify document files exist at specified paths
2. Check document content isn't empty
3. Verify ChromaDB collection is populated:
   ```python
   print(collection.count())  # Should be > 0
   ```
4. Try shorter, simpler queries

### Issue: "JSON decode error"

**Symptoms**: Max retries exceeded, error response

**Solutions**:
1. Check LLM response format in logs
2. Verify Pydantic schema in prompt template
3. Increase `max_retries` temporarily for debugging
4. Test with `MOCK_LLM = '1'` first

### Issue: "Model not available"

**Symptoms**: API 404 error

**Solutions**:
1. Verify Groq API key is set
2. Check model name: `qwen/qwen3.8-27b`
3. Confirm API quota limits not exceeded
4. Try alternative model in same tier

### Issue: "Slow response times"

**Symptoms**: > 5 seconds per query

**Solutions**:
1. Reduce `n_results` in retrieval (default: 3)
2. Check database connection
3. Monitor network latency to LLM API
4. Consider query batching for high volume

### Issue: "High memory usage"

**Symptoms**: OOM errors

**Solutions**:
1. Use `EphemeralClient()` for development
2. Reduce chunk size
3. Implement query queue with limits
4. Use persistent DB to avoid reindexing

## Advanced Configuration

### Custom Prompts

Edit the prompt templates to customize behavior:

```python
intent_classification_prompt_template = """..."""
answer_generation_prompt_template = """..."""
direct_answer_prompt_template = """..."""
```

### Custom Keywords

Add domain-specific keywords for classification:

```python
keywords.extend(["exchange", "warranty", "bulk order"])
```

### Custom Retrieval

Implement custom retrieval logic:

```python
def retrieve_custom(question, category_filter=None):
    # Add metadata filtering, re-ranking, etc.
    results = collection.query(
        query_texts=question,
        n_results=3,
        where={"source": category_filter} if category_filter else None
    )
    return results["documents"][0], results['metadatas'][0]
```

## Monitoring & Metrics

### Key Metrics to Track

```python
# Query volume
queries_per_minute = count_queries() / 60

# Classification accuracy
accuracy = correct_classifications / total_classifications

# Response latency
avg_latency = sum(response_times) / len(response_times)

# Confidence distribution
avg_confidence = sum(confidences) / len(confidences)

# Document coverage
docs_with_answers = count(confidence > 0.5) / total_queries
```

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Query: {query}")
logger.info(f"Intent: {intent}")
logger.info(f"Confidence: {confidence}")
```

## Future Enhancements

- [ ] Multi-turn conversation history
- [ ] User feedback loop for confidence calibration
- [ ] Fine-tuned embeddings for Zepto domain
- [ ] Document versioning and hot updates
- [ ] Analytics dashboard for query patterns
- [ ] Multi-language support
- [ ] Integration with ticket management system
- [ ] Custom intent categories (e.g., "billing", "technical")
- [ ] Response personalization based on user tier
- [ ] A/B testing framework for prompt improvements

## File Structure

```
SupportAssistances/
├── support_assistances.py     # Main implementation
├── SUPPORTREADME.md           # This file
├── requirements.txt           # Dependencies (optional)
└── .env.example              # Environment template (optional)
```

## Dependencies

```
chromadb
sentence-transformers
langgraph
pydantic
fastapi
uvicorn
nest-asyncio
groq  # For LLM API
```

## License

[Add appropriate license]

## Support & Contribution

For issues or improvements:
1. Check troubleshooting section above
2. Review logs for error details
3. Test with `MOCK_LLM = '1'` mode first
4. File issues with query examples and expected vs. actual output

---

**Version**: 1.0  
**Last Updated**: September 2026  
**Maintainer**: Zepto Support Team
