FROM python:3.11-slim

WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Создаём папку для данных
RUN mkdir -p /app/data && chmod 777 /app/data

# Команда запуска
CMD ["python", "bot.py"]
