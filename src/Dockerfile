# 1. Start with a lightweight, secure Python base image
FROM python:3.11-slim

# 2. Set up the working environment directory inside our virtual container
WORKDIR /app

# 3. Copy our system library requirements list over first
COPY requirements.txt .

# 4. Install dependencies directly into the core container environment
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all project assets across into the image architecture
COPY src/ ./src/
COPY data/ ./data/
COPY models/ ./models/

# 6. Open up network channels for both FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# 7. Create an entry point script layout to launch both backend and frontend servers
CMD uvicorn src.app:app --host 0.0.0.0 --port 8000 & streamlit run src/dashboard.py --server.port 8501 --server.address 0.0.0.0