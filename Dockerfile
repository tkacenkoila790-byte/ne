FROM python:3.10-slim

# Устанавливаем рабочую папку
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код бота
COPY . .

# Открываем порт, который требует Render
EXPOSE 8080

# Запускаем нашего бота
CMD ["python", "bot.py"]
