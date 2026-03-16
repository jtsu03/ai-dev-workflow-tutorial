FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project definition and install dependencies first (layer cache)
COPY pyproject.toml .
RUN uv pip install --system .

# Copy application source and data
COPY dashboard/ ./dashboard/
COPY data/ ./data/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "dashboard/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
