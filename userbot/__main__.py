import glob
import os
import sys
from pathlib import Path

import telethon.utils
from telethon import functions, types

import userbot
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.Config import Config
from userbot.core.logger import logging
from userbot.core.session import catub
from userbot.utils import load_module

LOGS = logging.getLogger("CatUserbot")

print(userbot.__copyright__)
print("Licensed under the terms of the " + userbot.__license__)


async def testing_bot():
    try:
        await catub.connect()
        config = await catub(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == catub.session.server_address:
                if catub.session.dc_id != option.id:
                    LOGS.warning(
                        f"Fixed DC ID in session from {catub.session.dc_id}"
                        f" to {option.id}"
                    )
                catub.session.set_dc(option.id, option.ip_address, option.port)
                catub.session.save()
                break
        await catub.start(bot_token=Config.TG_BOT_USERNAME)
        catub.me = await catub.get_me()
        catub.uid = telethon.utils.get_peer_id(catub.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {str(e)}")
        sys.exit()


def verifyLoggerGroup():
    if BOTLOG:
        try:
            entity = catub.loop.run_until_complete(catub.get_entity(BOTLOG_CHATID))
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified Logger group."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified Logger group."
                    )
        except ValueError:
            LOGS.error("Logger group ID cannot be found. " "Make sure it's correct.")
        except TypeError:
            LOGS.error("Logger group ID is unsupported. " "Make sure it's correct.")
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the logger group.\n"
                + str(e)
            )
    else:
        LOGS.info(
            "You haven't set the PRIVATE_GROUP_BOT_API_ID in vars please set it for proper functioning of userbot."
        )


async def add_bot_to_logger_group():
    try:
        bot_details = await catub.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        await catub(
            functions.messages.AddChatUserRequest(
                channel=BOTLOG_CHATID, users=bot_details.id, fwd_limit=1000000
            )
        )
    except Exception as e:
        LOGS.error(str(e))


async def startupmessage():
    if BOTLOG:
        await catub.tgbot.send_message(
            BOTLOG_CHATID,
            f"**Congratulation, now type {Config.COMMAND_HAND_LER}alive to see message if catub is working or not\
                \nIf you need assistance, **head to https://t.me/catuserbot_support",
            link_preview=False,
        )


if len(sys.argv) not in (1, 3, 4):
    catub.disconnect()
else:
    try:
        LOGS.info("Starting Userbot")
        catub.loop.run_until_complete(testing_bot())
        LOGS.info("Startup Completed")
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()


path = "userbot/plugins/*.py"
files = glob.glob(path)
files.sort()
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        try:
            if shortname.replace(".py", "") not in Config.NO_LOAD:
                load_module(shortname.replace(".py", ""))
            else:
                os.remove(Path(f"userbot/plugins/{shortname}.py"))
        except Exception as e:
            os.remove(Path(f"userbot/plugins/{shortname}.py"))
            LOGS.info(f"unable to load {shortname} because of error {e}")

path = "userbot/assistant/*.py"
files = glob.glob(path)
files.sort()
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        try:
            if shortname.replace(".py", "") not in Config.NO_LOAD:
                load_module(shortname.replace(".py", ""), plugin_path="userbot/assistant")
            else:
                os.remove(Path(f"userbot/assistant/{shortname}.py"))
        except Exception as e:
            os.remove(Path(f"userbot/assistant/{shortname}.py"))
            LOGS.info(f"unable to load {shortname} because of error {e}")

print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
print("Yay your userbot is officially working.!!!")
print(
    f"Congratulation, now type {Config.COMMAND_HAND_LER}alive to see message if catub is live\
      \nIf you need assistance, head to https://t.me/catuserbot_support"
)
print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")

verifyLoggerGroup()
catub.loop.create_task(add_bot_to_logger_group())
catub.loop.create_task(startupmessage())

if len(sys.argv) not in (1, 3, 4):
    catub.disconnect()
else:
    catub.run_until_disconnected()
