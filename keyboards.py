from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Asosiy menyu tugmalari: Kirim, Chiqim va Statistika."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1. Kirim"), KeyboardButton(text="2. Chiqim")],
            [KeyboardButton(text="3. Statistika")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Quyidagi tugmalardan birini tanlang..."
    )
    return keyboard

def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Amalni bekor qilish tugmasi."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_skip_keyboard() -> ReplyKeyboardMarkup:
    """Chiqim izohini o'tkazib yuborish yoki bekor qilish tugmalari."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="O'tkazib yuborish")],
            [KeyboardButton(text="Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard
