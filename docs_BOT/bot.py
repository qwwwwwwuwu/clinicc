from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import httpx


API_URL = "http://localhost:8000"
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(
        "Опишите ваши симптомы (например: 'болит зуб')"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    user_text = update.message.text
    
    
    doctor_specialty = ai_predict_specialty(user_text)  # stub
    
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/doctors/",
            params={"specialty": doctor_specialty}
        )
        slots = response.json()
    
   
    await update.message.reply_text(
        f"Рекомендую {doctor_specialty}. Свободные слоты:\n"
        + "\n".join([f"{s['time']} - {s['doctor']}" for s in slots])
    )

def ai_predict_specialty(text: str) -> str:
    
    
    if "зуб" in text.lower(): return "стоматолог"
    if "горло" in text.lower(): return "терапевт"
    return "терапевт"

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()