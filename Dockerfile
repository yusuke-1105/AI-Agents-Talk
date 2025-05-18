FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir streamlit anthropic

COPY . .

CMD ["streamlit", "run", "app.py"]