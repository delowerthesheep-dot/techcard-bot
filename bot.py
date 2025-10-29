import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен нового бота
BOT_TOKEN = os.environ.get('BOT_TOKEN', "8390604966:AAE39zuCSl9vfUjPZERJ2ncR8mTBrXr9rBU")

# На Render используем относительные пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# База данных напитков по категориям
DRINKS_DATABASE = {
    "Кофе": {
        "Афогато": os.path.join(BASE_DIR, "tech_cards", "Афогато.PNG"),
        "Капучино Вареная сгущенка с халвой": os.path.join(BASE_DIR, "tech_cards", "Капучино Вареная сгущенка с халвой.PNG"),
        "Эспрессо": os.path.join(BASE_DIR, "tech_cards", "Эспрессо.PNG"),
        "Латте": os.path.join(BASE_DIR, "tech_cards", "Латте.PNG"),
        "Американо": os.path.join(BASE_DIR, "tech_cards", "Американо.PNG"),
    },
    "Холодные напитки": {
        "Время лайма": os.path.join(BASE_DIR, "tech_cards", "Время лайма.PNG"),
        "Гуанабана": os.path.join(BASE_DIR, "tech_cards", "Гуанабана.PNG"),
        "Карибский ананас": os.path.join(BASE_DIR, "tech_cards", "Карибский ананас.PNG"),
        "Личи-драгонфрут": os.path.join(BASE_DIR, "tech_cards", "Личи-драгонфрут.PNG"),
        "Мохито": os.path.join(BASE_DIR, "tech_cards", "Мохито.PNG"),
    },
    "Сезонные напитки": {
        "Глинтвейн": os.path.join(BASE_DIR, "tech_cards", "Глинтвейн.PNG"),
        "Тыквенный латте": os.path.join(BASE_DIR, "tech_cards", "Тыквенный латте.PNG"),
        "Яблочный сидр": os.path.join(BASE_DIR, "tech_cards", "Яблочный сидр.PNG"),
    },
    "Чай": {
        "Молочный улун": os.path.join(BASE_DIR, "tech_cards", "Молочный улун.PNG"),
        "Эрл Грей": os.path.join(BASE_DIR, "tech_cards", "Эрл Грей.PNG"),
        "Зеленый чай": os.path.join(BASE_DIR, "tech_cards", "Зеленый чай.PNG"),
        "Чай масала": os.path.join(BASE_DIR, "tech_cards", "Чай масала.PNG"),
    },
    "Лимонады": {
        "Классический лимонад": os.path.join(BASE_DIR, "tech_cards", "Классический лимонад.PNG"),
        "Малиновый лимонад": os.path.join(BASE_DIR, "tech_cards", "Малиновый лимонад.PNG"),
        "Мятный лимонад": os.path.join(BASE_DIR, "tech_cards", "Мятный лимонад.PNG"),
    }
}

def create_main_keyboard():
    """Создает главную клавиатуру с категориями"""
    categories = list(DRINKS_DATABASE.keys())
    
    # Создаем кнопки категорий (по 2 в ряд)
    keyboard = []
    for i in range(0, len(categories), 2):
        row = []
        if i < len(categories):
            row.append(KeyboardButton(categories[i]))
        if i + 1 < len(categories):
            row.append(KeyboardButton(categories[i + 1]))
        keyboard.append(row)
    
    # Добавляем кнопку "Все напитки"
    keyboard.append([KeyboardButton("📋 Все напитки")])
    
    return ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True,
        input_field_placeholder="Выбери категорию напитков 👇"
    )

def create_category_keyboard(category):
    """Создает клавиатуру с напитками выбранной категории"""
    drinks = list(DRINKS_DATABASE[category].keys())
    
    # Создаем кнопки напитков (по 2 в ряд)
    keyboard = []
    for i in range(0, len(drinks), 2):
        row = []
        if i < len(drinks):
            row.append(KeyboardButton(drinks[i]))
        if i + 1 < len(drinks):
            row.append(KeyboardButton(drinks[i + 1]))
        keyboard.append(row)
    
    # Добавляем кнопки навигации
    keyboard.append([KeyboardButton("⬅️ Назад к категориям"), KeyboardButton("🏠 Главное меню")])
    
    return ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True,
        input_field_placeholder="Выбери напиток 👇"
    )

def create_all_drinks_keyboard():
    """Создает клавиатуру со всеми напитками"""
    all_drinks = []
    for category in DRINKS_DATABASE:
        all_drinks.extend(DRINKS_DATABASE[category].keys())
    
    # Создаем кнопки всех напитков (по 2 в ряд)
    keyboard = []
    for i in range(0, len(all_drinks), 2):
        row = []
        if i < len(all_drinks):
            row.append(KeyboardButton(all_drinks[i]))
        if i + 1 < len(all_drinks):
            row.append(KeyboardButton(all_drinks[i + 1]))
        keyboard.append(row)
    
    # Добавляем кнопки навигации
    keyboard.append([KeyboardButton("⬅️ Назад к категориям"), KeyboardButton("🏠 Главное меню")])
    
    return ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True,
        input_field_placeholder="Выбери напиток 👇"
    )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start - приветствие"""
    welcome_text = """
👋 Привет! Я бот для поиска техкарт напитков.

🏷️ **Как пользоваться:**
1. Выбери категорию напитков
2. Нажми на кнопку с названием напитка
3. Получи техкарту!

✨ Можно также написать название напитка вручную.

📊 **Всего напитков в базе:** {total_drinks}
""".format(total_drinks=sum(len(drinks) for drinks in DRINKS_DATABASE.values()))
    
    # Отправляем сообщение с главной клавиатурой
    await update.message.reply_text(
        welcome_text,
        reply_markup=create_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений и нажатий на кнопки"""
    user_message = update.message.text.strip()
    
    print(f"🔍 Пользователь написал: '{user_message}'")
    
    # Обработка навигационных кнопок
    if user_message == "🏠 Главное меню":
        await update.message.reply_text(
            "Возвращаемся в главное меню:",
            reply_markup=create_main_keyboard()
        )
        return
        
    elif user_message == "⬅️ Назад к категориям":
        await update.message.reply_text(
            "Выбери категорию напитков:",
            reply_markup=create_main_keyboard()
        )
        return
        
    elif user_message == "📋 Все напитки":
        all_drinks_count = sum(len(drinks) for drinks in DRINKS_DATABASE.values())
        await update.message.reply_text(
            f"🍹 Все напитки ({all_drinks_count}):",
            reply_markup=create_all_drinks_keyboard()
        )
        return
    
    # Проверяем категории
    if user_message in DRINKS_DATABASE:
        drinks_count = len(DRINKS_DATABASE[user_message])
        await update.message.reply_text(
            f"🍹 {user_message} ({drinks_count} напитков):",
            reply_markup=create_category_keyboard(user_message)
        )
        return
    
    # Ищем напиток в базе (по всем категориям)
    found_drink = None
    found_category = None
    
    for category, drinks in DRINKS_DATABASE.items():
        for drink in drinks:
            if user_message.lower() == drink.lower():
                found_drink = drink
                found_category = category
                break
        if found_drink:
            break
    
    if found_drink:
        file_path = DRINKS_DATABASE[found_category][found_drink]
        print(f"✅ Найден напиток: {found_drink} в категории: {found_category}")
        print(f"📁 Ищу файл по пути: {file_path}")
        print(f"📂 Файл существует: {os.path.exists(file_path)}")
        
        # Проверяем есть ли файл
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as photo:
                    # Отправляем фото
                    await update.message.reply_photo(
                        photo=photo,
                        caption=f"📋 {found_drink}\n🏷️ Категория: {found_category}"
                    )
                print(f"✅ Техкарта отправлена для: {found_drink}")
                
                # Показываем клавиатуру снова после отправки
                await update.message.reply_text(
                    "Выбери следующий напиток:",
                    reply_markup=create_main_keyboard()
                )
                
            except Exception as e:
                error_msg = f"❌ Ошибка при отправке техкарты: {str(e)}"
                print(error_msg)
                await update.message.reply_text(
                    "❌ Ошибка при отправке техкарты. Попробуйте еще раз.",
                    reply_markup=create_main_keyboard()
                )
        else:
            error_msg = f"❌ Файл техкарты для '{found_drink}' не найден"
            print(error_msg)
            
            await update.message.reply_text(
                f"❌ Техкарта для '{found_drink}' временно недоступна",
                reply_markup=create_main_keyboard()
            )
    else:
        # Если напиток не найден, показываем подсказку
        await update.message.reply_text(
            f"❌ Напиток '{user_message}' не найден.\n\n"
            f"Выбери категорию напитков ниже 👇",
            reply_markup=create_main_keyboard()
        )

async def show_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /menu - показать главное меню"""
    await update.message.reply_text(
        "🏠 Главное меню:",
        reply_markup=create_main_keyboard()
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ошибок"""
    logging.error(f"Ошибка: {context.error}")

def main():
    """Запуск бота"""
    print("✅ Бот запускается...")
    print(f"📁 Рабочая директория: {BASE_DIR}")
    print(f"🔑 Токен бота: {BOT_TOKEN[:10]}...")  # Показываем только начало токена для безопасности
    
    # Показываем структуру базы данных
    print("📊 Структура базы данных:")
    total_drinks = 0
    for category, drinks in DRINKS_DATABASE.items():
        drink_count = len(drinks)
        total_drinks += drink_count
        print(f"  🏷️ {category}: {drink_count} напитков")
        for drink in drinks:
            file_exists = "✅" if os.path.exists(DRINKS_DATABASE[category][drink]) else "❌"
            print(f"    {file_exists} {drink}")
    
    print(f"🍹 Всего напитков: {total_drinks}")
    
    try:
        # Создаем приложение бота
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("menu", show_menu_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Обработчик ошибок
        application.add_error_handler(error_handler)
        
        # Запускаем бота с обработкой конфликта
        print("🤖 Бот запущен и готов к работе!")
        print("🔄 Режим: polling")
        print("⏹️  Для остановки нажми Ctrl+C")
        
        # Запускаем с очисткой pending updates
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        print(f"❌ Критическая ошибка при запуске: {e}")
        print("🔄 Попытка перезапуска через 10 секунд...")
        import time
        time.sleep(10)
        main()  # Перезапускаем бота

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
