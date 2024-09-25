import logging
import os

# Проверяем наличие директории и создаем ее, если нужно
if not os.path.exists('data'):
    os.makedirs('data')

# Создаем второй логгер, который записывает логи только в файл
file_logger = logging.getLogger('file_logger')
file_logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логгера на DEBUG

# Создаем файловый обработчик (запись в файл)
file_handler = logging.FileHandler('data/logs.txt', mode='a')
file_handler.setLevel(logging.DEBUG)  # Логи начиная с уровня DEBUG

# Устанавливаем формат для логов
file_formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(file_formatter)

# Добавляем обработчик в логгер
file_logger.addHandler(file_handler)