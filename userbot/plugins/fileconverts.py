"""COMMAND : .ftoimg 
here file must be in image file """
import asyncio
from io import BytesIO
from telethon import types
from ..utils import admin_cmd, sudo_cmd
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import SendMediaRequest

@borg.on(admin_cmd(pattern="ftoi$"))
@borg.on(sudo_cmd(pattern="ftoi$",allow_sudo = True))
async def on_file_to_photo(event):
    target = await event.get_reply_message()
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith('image/'):
        return  # This isn't an image
    if image.mime_type == 'image/webp':
        return  # Telegram doesn't let you directly send stickers as photos
    if image.size > 10 * 1024 * 1024:
        return  # We'd get PhotoSaveFileInvalidError otherwise
    file = await borg.download_media(target, file=BytesIO())
    file.seek(0)
    img = await borg.upload_file(file)
    img.name = 'image.png'
    try:
        await borg(SendMediaRequest(
            peer=await event.get_input_chat(),
            media=types.InputMediaUploadedPhoto(img),
            message=target.message,
            entities=target.entities,
            reply_to_msg_id=target.id
        ))
    except PhotoInvalidDimensionsError:
        return
