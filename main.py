import logging
from src.config import bot
import handlers.commands
import handlers.admin
import handlers.callbacks

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='bunker_log.txt',
                    filemode='a'  # 'a' значит дозаписывать в конец файла, а не стирать старое
)

bot.infinity_polling(timeout=10, long_polling_timeout=5)
