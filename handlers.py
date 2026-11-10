from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import add_transaction, get_statistics, get_recent_transactions
from keyboards import get_main_keyboard, get_cancel_keyboard, get_skip_keyboard

router = Router()

# FSM holatlari (Kirim va Chiqim jarayonlari uchun)
class IncomeState(StatesGroup):
    waiting_for_amount = State()

class ExpenseState(StatesGroup):
    waiting_for_amount = State()
    waiting_for_comment = State()

def format_money(amount: float) -> str:
    """Raqamni 1 000 000 yoki 1 000 000.50 ko'rinishida formatlash."""
    if amount == int(amount):
        return f"{int(amount):,}".replace(",", " ")
    return f"{amount:,.2f}".replace(",", " ")

def parse_amount(text: str):
    """Foydalanuvchi yuborgan summani tekshirish va float ko'rinishiga o'tkazish."""
    cleaned = text.replace(" ", "").replace(",", ".")
    try:
        val = float(cleaned)
        if val <= 0:
            return None
        return val
    except ValueError:
        return None

# /start buyrug'i
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    text = (
        f"Assalomu alaykum, <b>{message.from_user.full_name}</b>!\n\n"
        "Shaxsiy <b>Telegram Hamyon</b> botingizga xush kelibsiz.\n"
        "Bu bot yordamida kirim va chiqimlaringizni qulay hisoblab borishingiz mumkin.\n\n"
        "Kerakli bo'limni tanlang:"
    )
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")

# Amalni bekor qilish
@router.message(F.text.casefold() == "bekor qilish")
@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Amal bekor qilindi. Bosh menyu:", reply_markup=get_main_keyboard())

# 1. Kirim bosilganda
@router.message(F.text.in_(["1. Kirim", "Kirim"]))
async def start_income(message: Message, state: FSMContext):
    await state.set_state(IncomeState.waiting_for_amount)
    await message.answer(
        "💰 <b>Qancha pul kirdi?</b>\nSummani kiriting (masalan: 50000 yoki 100 000):",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )

@router.message(IncomeState.waiting_for_amount)
async def process_income_amount(message: Message, state: FSMContext):
    amount = parse_amount(message.text)
    if amount is None:
        await message.answer(
            "⚠️ <b>Noto'g'ri summa kiritildi!</b>\nIltimos, faqat noldan katta musbat son kiriting (masalan: 150000):",
            reply_markup=get_cancel_keyboard(),
            parse_mode="HTML"
        )
        return

    add_transaction(
        user_id=message.from_user.id,
        tx_type="kirim",
        amount=amount,
        comment=None
    )
    await state.clear()
    await message.answer(
        f"✅ <b>Kirim muvaffaqiyatli saqlandi!</b>\n\n"
        f"💵 Summa: <b>+{format_money(amount)} so'm</b>",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )

# 2. Chiqim bosilganda
@router.message(F.text.in_(["2. Chiqim", "Chiqim"]))
async def start_expense(message: Message, state: FSMContext):
    await state.set_state(ExpenseState.waiting_for_amount)
    await message.answer(
        "💸 <b>Qancha pul chiqdi?</b>\nSummani kiriting (masalan: 20000 yoki 50 000):",
        reply_markup=get_cancel_keyboard(),
        parse_mode="HTML"
    )

@router.message(ExpenseState.waiting_for_amount)
async def process_expense_amount(message: Message, state: FSMContext):
    amount = parse_amount(message.text)
    if amount is None:
        await message.answer(
            "⚠️ <b>Noto'g'ri summa kiritildi!</b>\nIltimos, faqat noldan katta musbat son kiriting (masalan: 25000):",
            reply_markup=get_cancel_keyboard(),
            parse_mode="HTML"
        )
        return

    await state.update_data(amount=amount)
    await state.set_state(ExpenseState.waiting_for_comment)
    await message.answer(
        "📝 Chiqim uchun izoh qoldirasizmi? (masalan: <i>non, taksi, tushlik</i>)\n"
        "Izoh yozing yoki <b>O'tkazib yuborish</b> tugmasini bosing:",
        reply_markup=get_skip_keyboard(),
        parse_mode="HTML"
    )

@router.message(ExpenseState.waiting_for_comment)
async def process_expense_comment(message: Message, state: FSMContext):
    comment_text = message.text.strip()
    if comment_text.casefold() == "o'tkazib yuborish":
        comment_text = None

    data = await state.get_data()
    amount = data.get("amount")

    add_transaction(
        user_id=message.from_user.id,
        tx_type="chiqim",
        amount=amount,
        comment=comment_text
    )
    await state.clear()

    comment_msg = f"\n🏷 Izoh: <i>{comment_text}</i>" if comment_text else ""
    await message.answer(
        f"✅ <b>Chiqim muvaffaqiyatli saqlandi!</b>\n\n"
        f"💸 Summa: <b>-{format_money(amount)} so'm</b>{comment_msg}",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )

# 3. Statistika bosilganda
@router.message(F.text.in_(["3. Statistika", "Statistika"]))
async def show_statistics(message: Message):
    stats = get_statistics(message.from_user.id)
    recent = get_recent_transactions(message.from_user.id, limit=5)

    income_str = format_money(stats["income"])
    expense_str = format_money(stats["expense"])
    balance_str = format_money(stats["balance"])

    # Balans holatiga qarab belgi
    balance_icon = "🟢" if stats["balance"] >= 0 else "🔴"

    text = (
        "📊 <b>Moliya statistikangiz:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🟢 <b>Jami kirim:</b>  +{income_str} so'm\n"
        f"🔴 <b>Jami chiqim:</b> -{expense_str} so'm\n"
        f"{balance_icon} <b>Qolgan balans:</b> {balance_str} so'm\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🕒 <b>Oxirgi 5 ta amal:</b>\n"
    )

    if not recent:
        text += "<i>Hozircha hech qanday amallar mavjud emas.</i>"
    else:
        for idx, row in enumerate(recent, 1):
            t_type = row["type"]
            t_amount = format_money(row["amount"])
            t_date = row["created_at"]
            t_comment = f" ({row['comment']})" if row["comment"] else ""

            if t_type == "kirim":
                sign = "➕"
            else:
                sign = "➖"

            text += f"{idx}. {sign} {t_amount} so'm{t_comment} — <i>{t_date}</i>\n"

    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="HTML")
