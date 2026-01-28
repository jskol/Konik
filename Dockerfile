FROM python:3.11
ENV PYTHONUNBUFFERED=1
ENV RUN_IN_BACKGROUND=1
ENV UPLOAD_TO_HF=1
ENV HANDLE_HTTPS=1

# Tworzymy folder roboczy
WORKDIR /app

# Kopiujemy listę bibliotek i instalujemy je
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .
WORKDIR /app/WebApp

# Startujemy serwer uvicorn na porcie 7860
CMD ["uvicorn", "main_API:webapp", "--host", "0.0.0.0", "--port", "7860"]