# Rasmiy yengil Python imidji
FROM python:3.11-slim

# Ishchi papka
WORKDIR /app

# Muhit o'zgaruvchilari (keshni kamaytirish va loglarni darhol ko'rsatish)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Talab qilinadigan kutubxonalarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihaning qolgan barcha fayllarini ko'chirish
COPY . .

# Botni ishga tushirish buyrug'i
CMD ["python", "main.py"]
