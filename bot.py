import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
BOT_TOKEN = "8204345196:AAGa9ckArC5xUNSixAMtwTlY_NMGFYGnzDk"

# База напитков и их техкарт
DRINKS_DATABASE = {
    "Афогато": "tech_cards/Афогато.png",
    "Время лайма": "tech_cards/Время лайма.png",
    "Гуанабана": "tech_cards/Гуанабана.png",
    "Капучино Вареная сгущенка с халвой": "tech_cards/Капучино Сгущенка с халвой.png",
    "Карибский ананас": "tech_cards/Карибский ананас.png",
    "Личи-драгонфрут": "tech_cards/Личи-драгонфрут.png",
}

def create_drinks_keyboard():
    """Создает клавиатуру с кнопками напитков"""
    drinks = list(DRINKS_DATABASE.keys())
    
    # Создаем кнопки (по 2 в ряд для красоты)
    keyboard = []
    for i in range(0, len(drinks), 2):
        row = []
        if i < len(drinks):
            row.append(KeyboardButton(drinks[i]))
        if i + 1 < len(drinks):
            row.append(KeyboardButton(drinks[i + 1]))
        keyboard.append(row)
    
    # Добавляем кнопку "Показать все напитки"
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
    
    # Отправляем сообщение с клавиатурой
    await update.message.reply_text(
        welcome_text,
        reply_markup=create_drinks_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений и нажатий на кнопки"""
    user_message = update.message.text.strip()
    
    print(f"🔍 Пользователь написал: '{user_message}'")
    
    # Обработка кнопки "Показать все напитки"
    if user_message == "📋 Показать все напитки":
        available_drinks = "\n".join([f"• {drink}" for drink in DRINKS_DATABASE.keys()])
        await update.message.reply_text(
            f"🍹 Все доступные напитки:\n\n{available_drinks}\n\n"
            f"Нажми на кнопку с названием напитка 👆"
        )
        return
    
    # Ищем напиток в базе (точное совпадение)
    found_drink = None
    for drink in DRINKS_DATABASE:
        if user_message.lower() == drink.lower():
            found_drink = drink
            break
    
    if found_drink:
        file_path = DRINKS_DATABASE[found_drink]
        print(f"✅ Найден напиток: {found_drink}, путь: {file_path}")
        
        # Проверяем есть ли файл
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as photo:
                    # Сначала отправляем фото
                    await update.message.reply_photo(
                        photo=photo,
                        caption=f"📋 Техкарта: {found_drink}"
                    )
                print(f"✅ Техкарта отправлена для: {found_drink}")
                
                # Показываем клавиатуру снова после отправки
                await update.message.reply_text(
                    "Выбери следующий напиток:",
                    reply_markup=create_drinks_keyboard()
                )
                
            except Exception as e:
                await update.message.reply_text(
                    f"❌ Ошибка при отправке техкарты: {str(e)}",
                    reply_markup=create_drinks_keyboard()
                )
        else:
            await update.message.reply_text(
                f"❌ Файл техкарты для '{found_drink}' не найден\n"
                f"Путь: {file_path}",
                reply_markup=create_drinks_keyboard()
            )
    else:
        # Если напиток не найден, показываем подсказку
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
    # Создаем папку для техкарт
    os.makedirs("tech_cards", exist_ok=True)
    
    # Создаем приложение бота
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", show_menu_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("✅ Бот запущен и готов к работе!")
    print("📊 Напитки в базе:", list(DRINKS_DATABASE.keys()))
    print("⏹️  Чтобы остановить бота, нажми Ctrl+C")
    application.run_polling()

if __name__ == "__main__":
    main()