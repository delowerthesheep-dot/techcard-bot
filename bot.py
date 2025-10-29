import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8204345196:AAGa9ckArC5xUNSixAMtwTlY_NMGFYGnzDk')

# БАЗА НАПИТКОВ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DRINKS_DATABASE = {
    "Афогато": os.path.join(BASE_DIR, "tech_cards", "Афогато.PNG"),
    "Время лайма": os.path.join(BASE_DIR, "tech_cards", "Время лайма.PNG"),
    "Гуанабана": os.path.join(BASE_DIR, "tech_cards", "Гуанабана.PNG"),
    "Капучино Вареная сгущенка с халвой": os.path.join(BASE_DIR, "tech_cards", "Капучино Вареная сгущенка с халвой.PNG"),
    "Карибский ананас": os.path.join(BASE_DIR, "tech_cards", "Карибский ананас.PNG"),
    "Личи-драгонфрут": os.path.join(BASE_DIR, "tech_cards", "Личи-драгонфрут.PNG"),
}

def create_drinks_keyboard():
    """Создает клавиатуру с кнопками напитков"""
    drinks = list(DRINKS_DATABASE.keys())
    
    keyboard = []
    for i in range(0, len(drinks), 2):
        row = []
        if i < len(drinks):
            row.append(KeyboardButton(drinks[i]))
        if i + 1 < len(drinks):
            row.append(KeyboardButton(drinks[i + 1]))
        keyboard.append(row)
    
    keyboard.append([KeyboardButton("📋 Показать все напитки")])
    
    return ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True,
        input_field_placeholder="Выбери напиток или нажми кнопку ниже 👇"
    )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - приветствие"""
    welcome_text = """
👋 Привет! Я бот для поиска техкарт напитков.

📝 Просто нажми на кнопку с названием напитка ниже, и я отправлю его техкарту.

✨ Можно также написать название напитка вручную.
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=create_drinks_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений и нажатий на кнопки"""
    user_message = update.message.text.strip()
    
    print(f"🔍 Пользователь написал: '{user_message}'")
    
    if user_message == "📋 Показать все напитки":
        available_drinks = "\n".join([f"• {drink}" for drink in DRINKS_DATABASE.keys()])
        await update.message.reply_text(
            f"🍹 Все доступные напитки:\n\n{available_drinks}\n\n"
            f"Нажми на кнопку с названием напитка 👆"
        )
        return
    
    found_drink = None
    for drink in DRINKS_DATABASE:
        if user_message.lower() == drink.lower():
            found_drink = drink
            break
    
    if found_drink:
        file_path = DRINKS_DATABASE[found_drink]
        print(f"✅ Найден напиток: {found_drink}")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as photo_file:
                    photo_data = photo_file.read()
                
                await update.message.reply_photo(
                    photo=photo_data,
                    caption=f"📋 Техкарта: {found_drink}"
                )
                print(f"✅ Техкарта отправлена для: {found_drink}")
                
                await update.message.reply_text(
                    "Выбери следующий напиток:",
                    reply_markup=create_drinks_keyboard()
                )
                
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                await update.message.reply_text(
                    "❌ Ошибка отправки. Попробуй еще раз.",
                    reply_markup=create_drinks_keyboard()
                )
        else:
            print(f"❌ Файл не найден: {file_path}")
            await update.message.reply_text(
                f"❌ Техкарта для '{found_drink}' временно недоступна",
                reply_markup=create_drinks_keyboard()
            )
    else:
        await update.message.reply_text(
            f"❌ Напиток '{user_message}' не найден.\n\n"
            f"Нажми на кнопку с названием напитка ниже 👇",
            reply_markup=create_drinks_keyboard()
        )

async def show_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /menu - показать меню кнопок"""
    await update.message.reply_text(
        "🍹 Выбери напиток:",
        reply_markup=create_drinks_keyboard()
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ошибок"""
    logging.error(f"Ошибка: {context.error}")

def main():
    """Запуск бота"""
    print("🚀 Бот запускается на Render...")
    print("📊 Напитки в базе:", list(DRINKS_DATABASE.keys()))
    
    # Проверяем файлы
    print("🔍 Проверка файлов техкарт:")
    for drink, path in DRINKS_DATABASE.items():
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"  {exists} {drink}")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", show_menu_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    print("🤖 Бот запущен и работает 24/7!")
    application.run_polling()

if __name__ == "__main__":
    main()
