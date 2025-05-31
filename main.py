import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from llama_cpp import Llama

# TOKEN bot Telegram kamu
TELEGRAM_TOKEN = "7614084480:AAEvOO2OdfBgaVLt_dPhwPbMLRW7sKAY0Nc"

# Path model llama.cpp
MODEL_PATH = "models/gpt4all-lora-quantized.bin"  # Ganti sesuai model kamu

# Load model
llm = Llama(model_path=MODEL_PATH)

# Prompt sistem roleplay NSFW sederhana
system_prompt = """You are a helpful and flirty AI character for roleplay chat. You answer with playful and sometimes naughty replies. Keep it text only."""

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    prompt = f"""[INST] <<SYS>>{system_prompt}<</SYS>>
{user_text} [/INST]"""

    # Generate response
    output = llm(prompt, max_tokens=150, temperature=0.8, stop=["[/INST]"])
    reply = output['choices'][0]['text'].strip()

    await update.message.reply_text(reply)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
