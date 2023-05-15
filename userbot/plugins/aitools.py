# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Special Credits: @odi for Somnium <image gen>

from somnium import Somnium

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import ThabAi, reply_id
from ..sql_helper.globals import addgvar, gvarstatus
from . import catub, mention

catai = ThabAi()

plugin_category = "tools"


@catub.cat_cmd(
    pattern="genimg(?:\s|$)([\s\S]*)",
    command=("genimg", plugin_category),
    info={
        "header": "Create beautiful artwork using the power of AI.",
        "notes": "Best styles are V2s",
        "usage": [
            "{tr}genimg -l ( get list of artstyles )",
            "{tr}genimg -l <style-id> ( change the style )",
            "{tr}genimg <text> (generate)",
        ],
        "examples": [
            "{tr}genimg -l",
            "{tr}genimg -l 2000",
            "{tr}genimg Cat riding bike",
        ],
    },
)
async def gen_img(odi):
    "Generate an Image using the provided text with Somnium"
    reply_to_id = await reply_id(odi)
    query = odi.pattern_match.group(1)
    if not query:
        return await edit_delete(odi, "`What should I do ??`")

    catevent = await edit_or_reply(odi, "`Processing ...`")
    rstyles = {value: key for key, value in Somnium.Styles().items()}
    styleid = int(gvarstatus("DREAM_STYLE") or "2000")

    if query.startswith("-l"):
        query = query.replace("-l", "").strip()
        if query.isnumeric():
            if int(query) in rstyles:
                addgvar("DREAM_STYLE", int(query))
                return await edit_delete(
                    catevent, f"`Style changed to {rstyles[int(query)]}.`"
                )

            return await edit_delete(
                catevent,
                f"**Wrong style id.\n\n🎠 Here is list of:**  [styles]({Somnium.StylesGraph()}) ",
                link_preview=True,
                time=120,
            )

        return await edit_delete(
            catevent,
            f"**🎠 Here is list of:**  [styles]({Somnium.StylesGraph()}) ",
            link_preview=True,
            time=120,
        )
    await edit_or_reply(catevent, "`Generating ai image ...`")
    getart = Somnium.Generate(query, styleid)
    ig getart == None:
        return await edit_delete(odi, "`Process failed or contains NSFW.`")
    await catub.send_file(
        odi.chat_id,
        getart,
        force_document=True,
        reply_to=reply_to_id,
        caption=f"**Query:** `{query}`\n**Style:** `{rstyles[styleid]}`\n\n__Generated by__ {mention}",
    )
    await catevent.delete()


@catub.cat_cmd(
    pattern="gentxt(?:\s|$)([\s\S]*)",
    command=("gentxt", plugin_category),
    info={
        "header": "Generate GPT response with prompt using the power of AI.",
        "usage": "{tr}gentxt < text / reply >",
        "examples": "{tr}gentxt write a paragraph on cat",
    },
)
async def gen_txt(event):
    "Generate a GPT response using the provided text without any API key"
    query = event.pattern_match.group(1)
    reply = await event.get_reply_message()

    if not query and reply:
        query = reply.text
    if not query:
        return await edit_delete(event, "`What should I do ??`")

    catevent = await edit_or_reply(event, "`Generating ai response ...`")
    if generated_text := catai.get_response(query):
        await edit_or_reply(catevent, generated_text)
    else:
        await edit_delete(catevent, "`Sorry, unable to generate response`")
