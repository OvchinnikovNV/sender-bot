import os
from handlers.handler import bot
from log import logger


if __name__ == '__main__':
    if not os.path.exists( os.path.join( os.path.dirname(__file__ ), '.env' ) ):
        logger.critical('FIle .env don\'n exist!')
        exit(1)

    logger.info("Bot starting...")
    bot.infinity_polling()
    logger.success("Bot successfuly closed")
