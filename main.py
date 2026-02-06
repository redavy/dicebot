import logging
import asyncio
import os

from dotenv import load_dotenv
from pyrogram import Client, types, filters

logging.basicConfig(
    level = logging.INFO,
    format = "%(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

load_dotenv()

SESSION_NAME = os.getenv("SESSION_NAME")
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not all([SESSION_NAME, API_ID, API_HASH]):
    raise ValueError("Not all .env variables are set")

app = Client(
    name = SESSION_NAME,
    api_id = API_ID,
    api_hash = API_HASH
)


@app.on_message(filters.command("dice", prefixes = ".") & filters.me)
async def dice(client: Client, message: types.Message):
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.edit("Usage: `.dice 1-6`")
            await asyncio.sleep(2)
            await message.delete()
            return

        target = int(args[1])
        if target < 1 or target > 6:
            await message.edit("Target num must be from 1 to 6")
            await asyncio.sleep(2)
            await message.delete()
            return

        await message.delete()

        attempts = 0
        max_attempts = 50

        while attempts < max_attempts:
            attempts += 1
            
            dice = await client.send_dice(
                chat_id = message.chat.id,
                emoji = "🎲"
            )

            value = dice.dice.value
            if value == target:
                break

            await dice.delete()

    except Exception as e:
        error = await message.reply(f"Error: {str(e)}")
        await asyncio.sleep(2)
        await error.delete()
        await message.delete()


if __name__ == "__main__":
    logger.info("Starting dicebot...")
    logger.info("Send .dice 1-6 in any chat")
    logger.info("Press Ctrl+C to stop")
    app.run()
    logger.info("Exiting dicebot...")
