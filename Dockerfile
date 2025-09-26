FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -c "from langchain_community.embeddings import SentenceTransformerEmbeddings; SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')"

CMD ["python", "src/main.py"]