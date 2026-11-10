# Telegram Hamyon Boti

Telegram orqali shaxsiy daromad va xarajatlarni (kirim, chiqim, statistika va balans) hisoblab borish uchun qulay bot.

## Texnologiyalar
- **Python**: 3.11+
- **aiogram**: 3.x (asinxron Telegram bot kutubxonasi)
- **SQLite**: (ichki `sqlite3` moduli, ma'lumotlar bazasi fayli `hamyon.db`)
- **python-dotenv**: Tokenni `.env` faylidan xavfsiz o'qish uchun

---

## Papka tuzilishi
```
hamyon/
├── main.py              # Botni ishga tushirish fayli
├── database.py          # SQLite ma'lumotlar bazasi bilan ishlash funksiyalari
├── keyboards.py         # Tugmalar (ReplyKeyboard) menyusi
├── handlers.py          # Xabarlarni qabul qilish va FSM holatlari
├── .env                 # Maxfiy token saqlanadigan fayl (git'ga yuklanmaydi)
├── .env.example         # Token namunasi
├── requirements.txt     # Kerakli Python kutubxonalari
└── README.md            # Qo'llanma
```

---

## O'rnatish va ishga tushirish qadamlari

### 1. Papkaga kirish
Buyruqlar qatorini (Command Prompt yoki PowerShell) oching va loyiha papkasiga o'ting:
```bash
cd "C:\Users\777 comp service\Desktop\hamyon"
```

### 2. Virtual muhit yaratish (tavsiya etiladi)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Bot tokenini sozlash
1. Telegramda [@BotFather](https://t.me/BotFather) orqali yangi bot yarating va API tokenini oling.
2. `hamyon` papkasidagi `.env` faylini oching va tokenni yozing:
   ```env
   BOT_TOKEN=1234567890:AAExampleTokenHere...
   ```

### 5. Botni ishga tushirish
```bash
python main.py
```

---

## Bot imkoniyatlari
- **1. Kirim**: Daromad miqdorini kiritish, xatolarni tekshirish (faqat musbat sonlar) va bazaga yozish.
- **2. Chiqim**: Xarajat miqdorini kiritish hamda ixtiyoriy izoh (masalan: *tushlik, taksi*) qoldirish (yoki o'tkazib yuborish).
- **3. Statistika**:
  - Jami kirim
  - Jami chiqim
  - Qolgan sof balans (kirim - chiqim)
  - Oxirgi 5 ta amalning batafsil ro'yxati (summa, izoh, sana/vaqt)
- Har bir foydalanuvchining ma'lumotlari uning shaxsiy `user_id`si bo'yicha alohida saqlanadi.
- Summalar chiroyli bo'shliqlar bilan formatlanadi (masalan: `1 000 000 so'm`).
