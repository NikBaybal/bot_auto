FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1 

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

# установка зависимостей
RUN pip install --no-cache -r /app/requirements.txt

# запуск команды
CMD ["python", "./bot.py"]
