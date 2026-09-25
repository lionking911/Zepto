
#pip install chromadb sentence-transformers
import chromadb

with open("/content/drive/MyDrive/zapto1/Zepto/Delivery Policy", "r") as f:
  Delivery_Policy = f.read()
with open("/content/drive/MyDrive/zapto1/Zepto/Returns & Refunds", "r") as f:
  Return_Refunds = f.read()
with open("/content/drive/MyDrive/zapto1/Zepto/Membership Tiers", "r") as f:
  Membershipt_Tiers = f.read()
with open("/content/drive/MyDrive/zapto1/Zepto/Order Tracking", "r") as f:
  Order_Tracking = f.read()
with open("/content/drive/MyDrive/zapto1/Zepto/Order Cancellation Policy", "r") as f:
  Cancellation_Policy = f.read()
with open("/content/drive/MyDrive/zapto1/Zepto/Damaged or Missing Items", "r") as f:
   Missing_Items= f.read()
with open("/content/drive/MyDrive/zapto1/Zepto/Gift Cards", "r") as f:
  Gift_Cards = f.read()
with open("/content/drive/MyDrive/zapto1/Zepto/Customer Support Hours", "r") as f:
  Customer_Support_Hours = f.read()


def chunk_documents(text, source_name):

  paragraphs = text.strip().split("\n\n")
  chunks = []
  for para in paragraphs:
    para = para.strip()
    if len(para) < 50:
      continue

    if para.startswith("====="):
      continue

    chunks.append({
        "text": para,
        "source": source_name
    })

  return chunks

# Corrected indentation and source variables
Deliver_Policy_chunks=chunk_documents(Delivery_Policy,"Delivery Policy")
Returns_Refunds_chunks=chunk_documents(Return_Refunds,"Returns & Refunds")
Membership_Tiers_chunks=chunk_documents(Membershipt_Tiers,"Membership Tiers")
Order_Tracking_chunks=chunk_documents(Order_Tracking,"Order Tracking")
Order_Cancellation_Policy_chunks=chunk_documents(Cancellation_Policy,"Order Cancellation Policy")
Damaged_Missing_Items_chunks=chunk_documents(Missing_Items,"Damaged or Missing Items")
Gift_Cards_chunks=chunk_documents(Gift_Cards,"Gift Cards")
Customer_Support_Hours_chunks=chunk_documents(Customer_Support_Hours,"Customer Support Hours")

all_chunks=Deliver_Policy_chunks+Returns_Refunds_chunks+Membership_Tiers_chunks+Order_Tracking_chunks+Order_Cancellation_Policy_chunks+Damaged_Missing_Items_chunks+Gift_Cards_chunks+Customer_Support_Hours_chunks

# Using PersistentClient and get_or_create_collection for robustness
chroma_client = chromadb.PersistentClient(path="/content/zepto_knowledge_db")
collection = chroma_client.get_or_create_collection(name="compnay_docs")

documents = []
ids = []
metadata = []

for i, chunk in enumerate(all_chunks):
  documents.append(chunk['text'])
  ids.append(f"chunk_{i}")
  metadata.append({"source": chunk["source"]})

# Clear existing collection data if any, then add new documents
# This ensures idempotency when running the cell multiple times
if collection.count() > 0:
    collection.delete(ids=[id_ for id_ in collection.get()['ids']])

collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadata
)

def retrieve(question, n_results = 3):
  results = collection.query(
      query_texts = question,
      n_results = n_results
  )

  return results["documents"][0], results['metadatas'][0]

# Test the retrieve function
question = "What is the policy for canceling an order?"
retrieved_docs, retrieved_metadata = retrieve(question)

print("Retrieved Documents:")
for doc, meta in zip(retrieved_docs, retrieved_metadata):
  print(f"Source: {meta['source']}")
  print(f"Content: {doc}\n")



# Install LangGraph and Pydantic
!pip install -qU langgraph pydantic

# Import necessary libraries
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
import operator
import pandas as pd
from pydantic import BaseModel, Field
import json

# Define the State TypedDict
class AgentState(TypedDict):
    query: str
    intent: str
    answer: str
    retrieved_content: List[str]
    retrieved_metadata: List[dict]
    sources: List[str] # Added sources to AgentState
    confidence: float # Added confidence to AgentState

print(f"AgentState definition: {AgentState.__annotations__}")

# Define the Pydantic model for the final answer output
class AnswerOutput(BaseModel):
    answer: str = Field(description="The generated answer to the user's query.")
    sources: List[str] = Field(description="List of source document IDs or names used to generate the answer. Empty for general questions.")
    confidence: float = Field(description="A confidence score (0.0 to 1.0) for the generated answer.")

intent_classification_prompt_template = """You are an AI assistant tasked with classifying user queries. Your goal is to determine if a given query is a 'policy_question' related to Zepto's policies (e.g., delivery, returns, refunds, membership, tracking, cancellation, gift cards, support hours) or a 'general_question' (anything else).

Respond with ONLY one of the following two words: 'policy_question' or 'general_question xxxxx'.

Query: {query}
Classification:"""


def classify_intent(state: AgentState):
    #print("---CLASSIFY INTENT---")
    query = state["query"]
    intent = "general_question"

    if MOCK_LLM == '1': # Graded baseline: keyword heuristic
        keywords = ["delivery", "return", "refund", "membership", "tracking", "cancel", "gift card", "support hours"]
        if any(keyword in query.lower() for keyword in keywords):
            intent = "policy_question"
    else:
        
        prompt = intent_classification_prompt_template.format(query=query)
       
        # MOCK_LLM=0 extension: call the LLM to classify
        try:
            
            #print(f"Intent Classification Prompt: {prompt}") # Debug print
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="qwen/qwen3.8-27b", # Using a suitable Groq model for classification
                temperature=0.0
            )
            llm_response = chat_completion.choices[0].message.content.strip().lower()
            print(f"LLM Raw Intent Response: '{llm_response}'") # Debug print
            if llm_response == "policy_question": # Made comparison strict
                intent = "policy_question"
            else:
                intent = "general_question"
        except Exception as e:
            print(f"Error classifying intent with LLM: {e}")
            # Fallback to general question if LLM classification fails
            intent = "general_question"

    #print(f"Intent Classified : {intent}")
    return {"intent": intent}

answer_generation_prompt_template = """### Role
You are an AI assistant designed to answer questions based on provided context.

### Context
Use the following information to answer the user's query:

```text
{context}
```

### Task
Answer the user's question accurately and concisely, drawing solely from the provided context. If the answer is not present in the context, state that you cannot find the information. Specifically, answer the question: '{query}'

### Output Format
Your response MUST be a JSON object that adheres to the following Pydantic schema:
```json
{schema}
```

Ensure that:
- `answer` provides your response to the user's question (max 3 sentences).
- `sources` is a list of the *original document names* (e.g., 'Delivery Policy', 'Returns & Refunds') that were directly used to formulate the answer. If no specific documents were used (e.g., if you stated you couldn't find the information), this list should be empty.
- `confidence` is a float between 0.0 and 1.0, representing your certainty in the accuracy and completeness of the answer based *only* on the provided context.

### Negative Constraint
Do not use any outside knowledge or information that is not explicitly present in the provided `context`.

### Few-shot Example

**Example Input:**

**Role:** You are a helpful assistant.
**Context:** The sky is blue. Grass is green.
**Task:** What color is the sky?
**Output Format:** (as defined above)

**Expected Output:**
```json
{{"answer": "The sky is blue.", "sources": [], "confidence": 1.0}}
```"""

def retrieve_and_answer(state: AgentState):
    #print("---RETRIEVING AND ANSWERING---")
    query = state["query"]

    # Retrieval step always runs
    retrieved_docs, retrieved_metadata = retrieve(query)

    answer_output = None

    if MOCK_LLM == '1': # Graded baseline: canned templated answer with deterministic JSON
        # Use the first ~200 characters of the single most similar retrieved chunk
        top_chunk_snippet = retrieved_docs[0][:200] + "..." if retrieved_docs and len(retrieved_docs[0]) > 200 else (retrieved_docs[0] if retrieved_docs else "No relevant information found.")
        answer_text = f"Based on the retrieved context: {top_chunk_snippet}"
        sources_list = [meta['source'] for meta in retrieved_metadata]
        answer_output = AnswerOutput(answer=answer_text, sources=sources_list, confidence=1.0)
    else:
        # MOCK_LLM=0 extension: prompt the real LLM using structured template
        retries = 0
        max_retries = 2
        current_messages = []

        while retries <= max_retries:
            try:
                retrieved_context_parts = []
                for doc, meta in zip(retrieved_docs, retrieved_metadata):
                    retrieved_context_parts.append(f"Source: {meta['source']}\nContent: {doc}")

                formatted_context = "\n\n".join(retrieved_context_parts)
                pydantic_schema_str = json.dumps(AnswerOutput.model_json_schema(), indent=2)
                prompt = answer_generation_prompt_template.format(context=formatted_context, query=query,schema=pydantic_schema_str)
                
                if not current_messages: # First attempt
                    current_messages = [
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ]

                chat_completion = client.chat.completions.create(
                    messages=current_messages,
                    model="qwen/qwen3.8-27b", # Using a suitable Groq model for answer generation
                    temperature=0.0
                )
                llm_response_content = chat_completion.choices[0].message.content.strip()
                #print(f"LLM Raw Response (retrieve_and_answer): {llm_response_content}")

                # Attempt to parse JSON
                response_json = json.loads(llm_response_content)
                answer_output = AnswerOutput(**response_json)
                break # Successfully parsed and validated

            except json.JSONDecodeError as e:
                error_msg = f"JSON decoding error: {e}. Raw response: {llm_response_content}"
                #print(error_msg)
                if retries < max_retries:
                    corrective_instruction = f"Your previous response was not valid JSON. Please ensure your response is ONLY a valid JSON object adhering to the specified schema. Error: {e}."
                    current_messages.append({"role": "assistant", "content": llm_response_content})
                    current_messages.append({"role": "user", "content": corrective_instruction})
                    retries += 1
                else:
                    answer_output = AnswerOutput(answer="I encountered an error processing the response. Please try again.", sources=[], confidence=0.0)
                    print("Max retries reached for JSON decoding.")
                    break

            except Exception as e:
                error_msg = f"Error during LLM call or Pydantic validation: {e}. Raw response: {llm_response_content}"
                #print(error_msg)
                if retries < max_retries:
                    corrective_instruction = f"Your previous response failed validation: {e}. Please ensure your response is a valid JSON object adhering strictly to the schema including correct types and field names."
                    current_messages.append({"role": "assistant", "content": llm_response_content})
                    current_messages.append({"role": "user", "content": corrective_instruction})
                    retries += 1
                else:
                    answer_output = AnswerOutput(answer="I encountered an error processing the response. Please try again.", sources=[], confidence=0.0)
                    print("Max retries reached for LLM or Pydantic validation.")
                    break

        if answer_output is None:
             # Fallback if all retries fail or an unexpected issue occurs
             answer_output = AnswerOutput(answer="I encountered an unexpected error and could not generate a valid response. Please try again.", sources=[], confidence=0.0)

    #print(f"Answer generated: {answer_output.answer}")
    #print(f"Sources: {answer_output.sources}")
    #print(f"Confidence: {answer_output.confidence}")
    #print(f"Returning from retrieve_and_answer: {answer_output.dict()}")

    return {"answer": answer_output.answer, "retrieved_content": retrieved_docs, "retrieved_metadata": retrieved_metadata, "sources": answer_output.sources, "confidence": answer_output.confidence}


direct_answer_prompt_template = """### Role
You are an AI assistant for Zepto. Your primary function is to answer questions related to Zepto's policies. If a user asks a question that is outside the scope of Zepto's policies (e.g., general knowledge, personal opinions, or unrelated topics), you should politely decline to answer and state that you can only provide information about Zepto policies.

Query: {query}

### Output Format
Your response MUST be a JSON object that adheres to the following Pydantic schema:
```json
{schema}
```

Ensure that:
- `answer` provides your response to the user's query.
- `sources` is an empty list, as no documents are retrieved for general questions.
- `confidence` is a float between 0.0 and 1.0, representing your certainty in the accuracy of your response.

### Few-shot Example

**Example Input:**

**Role:** You are an AI assistant for Zepto.
**Query:** What is the capital of France?
**Output Format:** (as defined above)

**Expected Output:**
```json
{{"answer": "I can only answer questions about Zepto policies right now.", "sources": [], "confidence": 1.0}}
```"""

def direct_answer(state: AgentState):
    #print("--PROVIDING DIRECT ANSWER---")
    query = state["query"]
    answer_output = None

    if MOCK_LLM == '1': # Graded baseline: fixed canned string with deterministic JSON
        answer_output = AnswerOutput(answer="I can only answer questions about Zepto policies right now.", sources=[], confidence=1.0)
    else:
        # MOCK_LLM=0 extension: prompt the LLM directly, with no retrieval
        retries = 0
        max_retries = 2
        current_messages = []

        while retries <= max_retries:
            try:
                print(query)
                pydantic_schema_str = json.dumps(AnswerOutput.model_json_schema(), indent=2)
                prompt = direct_answer_prompt_template.format(query=query,schema=pydantic_schema_str)
                print(f"Direct Answer Prompt: {prompt}") # Debug print
                
                if not current_messages: # First attempt
                    current_messages = [
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ]

                chat_completion = client.chat.completions.create(
                    messages=current_messages,
                    model="qwen/qwen3.8-27b", # Using a suitable Groq model for direct answering
                    temperature=0.0
                )
                llm_response_content = chat_completion.choices[0].message.content.strip()
                #print(f"LLM Raw Response (direct_answer): {llm_response_content}")

                # Attempt to parse JSON
                response_json = json.loads(llm_response_content)
                answer_output = AnswerOutput(**response_json)
                break # Successfully parsed and validated

            except json.JSONDecodeError as e:
                error_msg = f"JSON decoding error: {e}. Raw response: {llm_response_content}"
                print(error_msg)
                if retries < max_retries:
                    corrective_instruction = f"Your previous response was not valid JSON. Please ensure your response is ONLY a valid JSON object adhering to the specified schema. Error: {e}."
                    current_messages.append({"role": "assistant", "content": llm_response_content})
                    current_messages.append({"role": "user", "content": corrective_instruction})
                    retries += 1
                else:
                    answer_output = AnswerOutput(answer="I encountered an error processing the response. Please try again.", sources=[], confidence=0.0)
                    print("Max retries reached for JSON decoding.")
                    break

            except Exception as e:
                error_msg = f"Error during LLM call or Pydantic validation: {e}. Raw response: {llm_response_content}"
                print(error_msg)
                if retries < max_retries:
                    corrective_instruction = f"Your previous response failed validation: {e}. Please ensure your response is a valid JSON object adhering strictly to the schema including correct types and field names."
                    current_messages.append({"role": "assistant", "content": llm_response_content})
                    current_messages.append({"role": "user", "content": corrective_instruction})
                    retries += 1
                else:
                    answer_output = AnswerOutput(answer="I encountered an error processing the response. Please try again.", sources=[], confidence=0.0)
                    print("Max retries reached for LLM or Pydantic validation.")
                    break

        if answer_output is None:
             # Fallback if all retries fail or an unexpected issue occurs
             answer_output = AnswerOutput(answer="I encountered an unexpected error and could not generate a valid response. Please try again.", sources=[], confidence=0.0)

    #print(f"Answer generated: {answer_output.answer}")
    #print(f"Sources: {answer_output.sources}")
    #print(f"Confidence: {answer_output.confidence}")
    #print(f"Returning from direct_answer: {answer_output.dict()}")

    return {"answer": answer_output.answer, "sources": answer_output.sources, "confidence": answer_output.confidence}

def route_intent(state: AgentState):
    print("--Route Intent---")
    if state["intent"] == "policy_question":
        print("i am here")
        return "retrieve_and_answer"
    elif state["intent"] == "general_question":
        print("general question")
        return "direct_answer"
    return "direct_answer" # Fallback
  
workflow = StateGraph(AgentState)

# Add nodes
#workflow.add_node("classifying_intent",classifying_intent)
workflow.add_node("classify_intent", classify_intent)
workflow.add_node("retrieve_and_answer", retrieve_and_answer)
workflow.add_node("direct_answer", direct_answer)

# Set the entry point
workflow.set_entry_point("classify_intent")

# Add edges
workflow.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer",
    },
)

# Set end points
workflow.add_edge("retrieve_and_answer", END)
workflow.add_edge("direct_answer", END)

# Compile the graph
apple = workflow.compile()

print("LangGraph StateGraph created successfully!")

# Set MOCK_LLM to '0' to use the real LLM integration
MOCK_LLM = '0'

#print("---Testing with a Policy Question---")
policy_query = "What is the policy for returns?"

# Run the graph
inputs = {"query": policy_query}
response = apple.invoke(inputs)

print(f"\nQuery: {response['query']}")
print(f"Intent: {response['intent']}")
print(f"Answer: {response['answer']}")
print(f"Retrieved Content Sources: {response['sources']}")
print(f"Confidence: {response['confidence']}")

# Set MOCK_LLM to '0' to use the real LLM integration
MOCK_LLM = '1'

print("\n---Testing with a General Question---")
general_query = "What is the capital of France?"

# Run the graph
inputs = {"query": general_query}
response = app.invoke(inputs)

print(f"\nQuery: {response['query']}")
print(f"Intent: {response['intent']}")
print(f"Answer: {response['answer']}")
print(f"Retrieved Content Sources: {response['sources']}")
print(f"Confidence: {response['confidence']}")

from fastapi import FastAPI

from pydantic import BaseModel
import nest_asyncio
import uvicorn
import threading 

nest_asyncio.apply()

# 6. Set up FastAPI
appp = FastAPI(title="LangGraph Agent API")

# Request schema for API input
class QueryRequest(BaseModel):
    user_query: str


MOCK_LLM = '0'
@appp.post("/chat")
async def chat_with_agent(request: QueryRequest):
    inputs = {"query": request.user_query}
    
    
    final_output = apple.invoke(inputs)
    return {"detected_intent": final_output["intent"], "agent_response": final_output["response"]}

# 5. Run Uvicorn in the background thread
def run_server():
    uvicorn.run(appp, host="127.0.0.1", port=8050)

threading.Thread(target=run_server, daemon=True).start()

# 6. Expose the server using localtunnel
print("\n👉 Click the link below when it appears. If it asks for an IP, use your Colab external IP.")
!npx --yes localtunnel --port 8050
