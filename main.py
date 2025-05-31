import os
from llama_cpp import Llama
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ==== SETUP ====
TELEGRAM_TOKEN = "7614084480:AAEvOO2OdfBgaVLt_dPhwPbMLRW7sKAY0Nc"  # Ganti dengan token bot kamu
MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

# Load prompt sistem
with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# Load LLM
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    n_gpu_layers=0,
    temperature=0.75,
    repeat_penalty=1.1,
    verbose=False
)

# Fungsi handle chat
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    prompt = f"""[INST] <<SYS>>{system_prompt}<</SYS>>
{user_input} [/INST]
"""
    output = llm(prompt, max_tokens=300, stop=["</s>"])
    reply = output["choices"][0]["text"].strip()
    await update.message.reply_text(reply)

# Start Bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
