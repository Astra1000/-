import os
from importlib import import_module
from pyrogram import Client, filters
from pyrogram.types import Message

# Конфигурация
API_ID = input("Введите api_id: ")
API_HASH = input("Введите api_hash: ")
PREFIX = "."
CMD_DIR = "cmd"

app = Client(
    "CUB",
    api_id=API_ID,
    api_hash=API_HASH,
    device_model="Cosmo",
    app_version="CUB 1.0",
    system_version="1.0"
)

# Загрузка команд из папки cmd
def load_commands():
    commands = {}
    if not os.path.exists(CMD_DIR):
        os.makedirs(CMD_DIR)
        print(f"Создана папка {CMD_DIR}. Добавьте туда файлы с командами.")
        return commands

    for filename in os.listdir(CMD_DIR):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                module_name = filename[:-3]
                module = import_module(f"{CMD_DIR}.{module_name}")
                if hasattr(module, "handle"):
                    commands[module_name] = module.handle
                    print(f"Команда {module_name} загружена")
            except Exception as e:
                print(f"Ошибка при загрузке {filename}: {e}")
    return commands

commands = load_commands()

# Обработчик сообщений
@app.on_message(filters.text & filters.private | filters.group)
async def handle_commands(client: Client, message: Message):
    if not message.text.startswith(PREFIX):
        return

    # Удаляем префикс и разбиваем на команду и аргументы
    command_parts = message.text[len(PREFIX):].split(maxsplit=1)
    command_name = command_parts[0].lower()
    args = command_parts[1] if len(command_parts) > 1 else ""

    if command_name in commands:
        await commands[command_name](client, message, args)

if __name__ == "__main__":
    print("Стартуем")
    app.run()
    print("Успешная остановка бота")
