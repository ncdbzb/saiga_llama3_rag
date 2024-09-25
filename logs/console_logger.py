import logging

# Создаем первый логгер, который выводит логи в консоль
console_logger = logging.getLogger('console_logger')
console_logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логгера на DEBUG

# Создаем консольный обработчик (вывод в консоль)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Логи начиная с уровня DEBUG

# Устанавливаем формат для логов
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)

# Добавляем обработчик в логгер
console_logger.addHandler(console_handler)
