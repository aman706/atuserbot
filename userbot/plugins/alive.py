import time
from platform import python_version

from telethon import version

from ..Config import Config
from . import (
    StartTime,
    catub,
    catversion,
    check_data_base_heal_th,
    edit_or_reply,
    get_readable_time,
    mention,
    reply_id,
)

CUSTOM_ALIVE_TEXT = Config.CUSTOM_ALIVE_TEXT or "✮ MY BOT IS RUNNING SUCCESSFULLY ✮"
EMOJI = Config.CUSTOM_ALIVE_EMOJI or "  ✥ "

plugin_category = "utils"


@catub.cat_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    if Config.ALIVE_PIC:
        cat_caption = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        cat_caption += f"**{EMOJI} Database :** `{check_sgnirts}`\n"
        cat_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
        cat_caption += f"**{EMOJI} Catuserbot Version :** `{catversion}`\n"
        cat_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
        cat_caption += f"**{EMOJI} Uptime :** `{uptime}\n`"
        cat_caption += f"**{EMOJI} Master:** {mention}\n"
        await event.client.send_file(
            event.chat_id, Config.ALIVE_PIC, caption=cat_caption, reply_to=reply_to_id
        )
        await event.delete()
    else:
        await edit_or_reply(
            event,
            f"**{CUSTOM_ALIVE_TEXT}**\n\n"
            f"**{EMOJI} Database :** `{check_sgnirts}`\n"
            f"**{EMOJI} Telethon Version :** `{version.__version__}\n`"
            f"**{EMOJI} Catuserbot Version :** `{catversion}`\n"
            f"**{EMOJI} Python Version :** `{python_version()}\n`"
            f"**{EMOJI} Uptime :** `{uptime}\n`"
            f"**{EMOJI} Master:** {mention}\n",
        )


@catub.cat_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    cat_caption = f"**Catuserbot is Up and Running**\n"
    cat_caption += f"**  -Telethon version :** `{version.__version__}\n`"
    cat_caption += f"**  -Catuserbot Version :** `{catversion}`\n"
    cat_caption += f"**  -Python Version :** `{python_version()}\n`"
    cat_caption += f"**  -Master:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()
