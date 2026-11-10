import sqlite3
import os
from datetime import datetime

# Ma'lumotlar bazasi fayl yo'li
DB_PATH = os.path.join(os.path.dirname(__file__), "hamyon.db")

def get_connection():
    """SQLite ma'lumotlar bazasiga ulanish obyekti qaytaradi."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Jadvallarni yaratish va bazani ishga tushirish."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('kirim', 'chiqim')),
            amount REAL NOT NULL,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON transactions (user_id)")
    conn.commit()
    conn.close()

def add_transaction(user_id: int, tx_type: str, amount: float, comment: str = None) -> int:
    """Yangi tranzaksiyani (kirim yoki chiqim) bazaga qo'shish."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO transactions (user_id, type, amount, comment, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, tx_type, amount, comment, now_str))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_statistics(user_id: int) -> dict:
    """Foydalanuvchining jami kirim, chiqim va joriy balansini hisoblaydi."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Jami kirim
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = ? AND type = 'kirim'", (user_id,))
    total_income = cursor.fetchone()[0]
    
    # Jami chiqim
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = ? AND type = 'chiqim'", (user_id,))
    total_expense = cursor.fetchone()[0]
    
    balance = total_income - total_expense
    
    conn.close()
    return {
        "income": total_income,
        "expense": total_expense,
        "balance": balance
    }

def get_recent_transactions(user_id: int, limit: int = 5) -> list:
    """Foydalanuvchining oxirgi kiritilgan amallari ro'yxatini qaytaradi."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, amount, comment, created_at
        FROM transactions
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows
