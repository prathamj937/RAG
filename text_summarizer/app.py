import chainlit as cl
import os
from summary import summarize_text, extract_text_from_file

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@cl.on_chat_start
async def start():
    await cl.Message("👋 Welcome to EY Smart Summarizer.\nUpload a `.pdf`, `.docx`, or `.txt` file to begin.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    if message.elements:
        file = message.elements[0]
        file_path = os.path.join(UPLOAD_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.content)

        try:
            content = extract_text_from_file(file_path)
        except Exception as e:
            await cl.Message(f"❌ Failed to process file: {e}").send()
            return

        await cl.Message("🔍 Summarizing your document...").send()
        summary = summarize_text(content)
        await cl.Message(f"✅ Summary of **{file.name}**:\n\n{summary}").send()
    else:
        content = message.content
        await cl.Message("🔍 Summarizing your text...").send()
        summary = summarize_text(content)
        await cl.Message(f"✅ Summary:\n\n{summary}").send()
