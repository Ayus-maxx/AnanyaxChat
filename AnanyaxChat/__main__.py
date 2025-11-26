import sys
import asyncio
import importlib
import logging
import threading
import config
from AnanyaxChat import ID_CHATBOT
from pyrogram import idle
from pyrogram.types import BotCommand
from config import OWNER_ID
from AnanyaxChat import LOGGER, AnanyaxChat, userbot, load_clone_owners
from AnanyaxChat.modules import ALL_MODULES
from AnanyaxChat.modules.Clone import restart_bots
from AnanyaxChat.modules.Id_Clone import restart_idchatbots

from colorama import Fore, Style, init
init(autoreset=True)

# --- Ensure default event loop policy (fixes "no current event loop" on Python 3.11+ / Heroku) ---
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: Fore.CYAN + "🐞 [DEBUG] " + Style.RESET_ALL + "%(message)s",
        logging.INFO: Fore.GREEN + "ℹ️ [INFO] " + Style.RESET_ALL + "%(message)s",
        logging.WARNING: Fore.YELLOW + "⚠️ [WARNING] " + Style.RESET_ALL + "%(message)s",
        logging.ERROR: Fore.RED + "❌ [ERROR] " + Style.RESET_ALL + "%(message)s",
        logging.CRITICAL: Fore.MAGENTA + "💥 [CRITICAL] " + Style.RESET_ALL + "%(message)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)


async def anony_boot():
    try:
        # Start main bot client
        await AnanyaxChat.start()
        try:
            # notify owner that bot started; using username to avoid undefined variable
            await AnanyaxChat.send_message(
                int(OWNER_ID),
                f"✨ @{AnanyaxChat.username} is now <b>Alive & Running ✅</b>"
            )
            LOGGER.info(f"🚀 @{AnanyaxChat.username} Started Successfully ✅")
        except Exception:
            LOGGER.warning(f"⚡ Please start @{AnanyaxChat.username} from the owner account.")

        # Restart clones (tasks)
        asyncio.create_task(restart_bots())
        asyncio.create_task(restart_idchatbots())

        # Load clone owners (await if it is async)
        await load_clone_owners()

        # If there's a userbot string configured, start it
        if getattr(config, "STRING1", None):
            try:
                await userbot.start()
                try:
                    await AnanyaxChat.send_message(int(OWNER_ID), "🤖 Id-Chatbot Also Started ✅")
                    LOGGER.info("🤖 Id-Chatbot started successfully ✅")
                except Exception:
                    LOGGER.warning("⚡ Please start Id-Chatbot from the owner account.")
            except Exception as ex:
                LOGGER.error(f"❌ Error in starting Id-Chatbot :- {ex}")
    except Exception as ex:
        LOGGER.critical(f"🔥 Bot failed to start: {ex}")

    # ----------------
    # Module Loader
    # ----------------
    for all_module in ALL_MODULES:
        try:
            importlib.import_module("AnanyaxChat.modules." + all_module)
            LOGGER.info(f"📦 Loaded Module: {Fore.CYAN}{all_module}{Style.RESET_ALL}")
        except Exception as e:
            LOGGER.error(f"❌ Failed to load module {all_module}: {e}")

    # ----------------
    # Bot Commands
    # ----------------
    try:
        await AnanyaxChat.set_bot_commands(
            commands=[
                BotCommand("start", "Start the bot"),
                BotCommand("help", "Get the help menu"),
                BotCommand("clone", "Make your own chatbot"),
                BotCommand("idclone", "Make your id-chatbot"),
                BotCommand("cloned", "Get List of all cloned bot"),
                BotCommand("ping", "Check if the bot is alive or dead"),
                BotCommand("lang", "Select bot reply language"),
                BotCommand("chatlang", "Get current using lang for chat"),
                BotCommand("resetlang", "Reset to default bot reply lang"),
                BotCommand("id", "Get users user_id"),
                BotCommand("stats", "Check bot stats"),
                BotCommand("gcast", "Broadcast any message to groups/users"),
                BotCommand("chatbot", "Enable or disable chatbot"),
                BotCommand("status", "Check chatbot enable or disable in chat"),
                BotCommand("shayri", "Get random shayri for love"),
                BotCommand("ask", "Ask anything from ChatGPT"),
            ]
        )
        LOGGER.info("✅ Bot commands set successfully.")
    except Exception as ex:
        LOGGER.error(f"❌ Failed to set bot commands: {ex}")

    LOGGER.info(f"🎉 @{AnanyaxChat.username} is fully up & running! 🚀")
    await idle()


# 🚀 Start Point
if __name__ == "__main__":
    # Use asyncio.run() which creates and manages the event loop correctly
    try:
        asyncio.run(anony_boot())
    except KeyboardInterrupt:
        LOGGER.info("🛑 Stopping AnanyaxChat Bot...")
    except Exception as e:
        LOGGER.critical(f"🔥 Unhandled error while running bot: {e}")
