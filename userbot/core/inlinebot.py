import json
import os
import re
import time

from telethon import Button, events

from userbot import catub

from ..Config import Config

CAT_IMG = Config.ALIVE_PIC or None
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")


def ibuild_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb


@catub.tgbot.on(events.InlineQuery)
async def inline_handler(event):  # sourcery no-metrics
    builder = event.builder
    result = None
    query = event.text
    hmm = re.compile("secret (.*) (.*)")
    match = re.findall(hmm, query)
    if query.startswith("**Catuserbot") and event.query.user_id == catub.uid:
        buttons = [
            (
                Button.inline("Stats", data="stats"),
                Button.url("Repo", "https://github.com/sandy1709/catuserbot"),
            )
        ]
        if CAT_IMG and CAT_IMG.endswith((".jpg", ".png")):
            result = builder.photo(
                CAT_IMG,
                # title="Alive cat",
                text=query,
                buttons=buttons,
            )
        elif CAT_IMG:
            result = builder.document(
                CAT_IMG,
                title="Alive cat",
                text=query,
                buttons=buttons,
            )
        else:
            result = builder.article(
                title="Alive cat",
                text=query,
                buttons=buttons,
            )
        await event.answer([result] if result else None)
    elif event.query.user_id == catub.uid and query.startswith("Inline buttons"):
        markdown_note = query[14:]
        prev = 0
        note_data = ""
        buttons = []
        for match in BTN_URL_REGEX.finditer(markdown_note):
            # Check if btnurl is escaped
            n_escapes = 0
            to_check = match.start(1) - 1
            while to_check > 0 and markdown_note[to_check] == "\\":
                n_escapes += 1
                to_check -= 1
            # if even, not escaped -> create button
            if n_escapes % 2 == 0:
                # create a thruple with button label, url, and newline
                # status
                buttons.append((match.group(2), match.group(3), bool(match.group(4))))
                note_data += markdown_note[prev : match.start(1)]
                prev = match.end(1)
            # if odd, escaped -> move along
            elif n_escapes % 2 == 1:
                note_data += markdown_note[prev:to_check]
                prev = match.start(1) - 1
            else:
                break
        else:
            note_data += markdown_note[prev:]
        message_text = note_data.strip()
        tl_ib_buttons = ibuild_keyboard(buttons)
        result = builder.article(
            title="Inline creator",
            text=message_text,
            buttons=tl_ib_buttons,
            link_preview=False,
        )
        await event.answer([result] if result else None)
    elif event.query.user_id == catub.uid and match:
        query = query[7:]
        user, txct = query.split(" ", 1)
        builder = event.builder
        secret = os.path.join("./userbot", "secrets.txt")
        try:
            jsondata = json.load(open(secret))
        except Exception:
            jsondata = False
        try:
            # if u is user id
            u = int(user)
            try:
                u = await event.client.get_entity(u)
                if u.username:
                    sandy = f"@{u.username}"
                else:
                    sandy = f"[{u.first_name}](tg://user?id={u.id})"
            except ValueError:
                # ValueError: Could not find the input entity
                sandy = f"[user](tg://user?id={u})"
        except ValueError:
            # if u is username
            try:
                u = await event.client.get_entity(user)
            except ValueError:
                return
            if u.username:
                sandy = f"@{u.username}"
            else:
                sandy = f"[{u.first_name}](tg://user?id={u.id})"
            u = int(u.id)
        except Exception:
            return
        timestamp = int(time.time() * 2)
        newsecret = {str(timestamp): {"userid": u, "text": txct}}

        buttons = [Button.inline("show message 🔐", data=f"secret_{timestamp}")]
        result = builder.article(
            title="secret message",
            text=f"🔒 A whisper message to {sandy}, Only he/she can open it.",
            buttons=buttons,
        )
        await event.answer([result] if result else None)
        if jsondata:
            jsondata.update(newsecret)
            json.dump(jsondata, open(secret, "w"))
        else:
            json.dump(newsecret, open(secret, "w"))


@catub.tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if os.path.exists("./userbot/secrets.txt"):
        jsondata = json.load(open("./userbot/secrets.txt"))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = [userid, catub.uid]
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
            else:
                reply_pop_up_alert = "why were you looking at this shit go away and do your own work, idiot"
        except KeyError:
            reply_pop_up_alert = "This message no longer exists in catub server"
    else:
        reply_pop_up_alert = "This message no longer exists "
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


@catub.tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == catub.uid:
        await event.edit("menu closed")
    else:
        reply_pop_up_alert = "Please get your own catuserbot, and don't use mine! Join @catuserbot17 help "
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


@catub.tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive()
    reply_pop_up_alert = statstext
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)