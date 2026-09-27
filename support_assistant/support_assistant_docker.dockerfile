FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (cached layer — only rebuilds if requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY support_assistances.py .


# Copy the company documents the RAG system searches through
COPY _data/ ./_data/

CMD ["uvicorn", "support_assistances:app", "--host", "0.0.0.0", "--port", "7860"]