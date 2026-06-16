from telegram import Update
from telegram.ext import ContextTypes
from io import BytesIO
import qrcode


async def qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command to generate QR code for a given text.
    """
    if update.message.text == "/qr":
        await update.message.reply_text("Please provide a text to generate QR code.")
        return
    text = " ".join(context.args)

    qr_image = qrcode.make(text)

    buffer = BytesIO()
    qr_image.save(buffer)
    buffer.seek(0)

    await update.message.reply_photo(photo=buffer, caption=f"QR Code for: {text}")
