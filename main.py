import os, asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import gdown, glob

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING = os.environ.get("STRING")
CHAT_ID = int(os.environ.get("CHAT_ID"))

FOLDER_LINK = "https://drive.google.com/drive/folders/14pY4V62ImG6g6XpkPFD2Y6IJDX9SlNKM?usp=drive_link" # https://drive.google.com/drive/folders/xxxx wala

async def main():
    sent = set(open("sent.txt").read().splitlines()) if os.path.exists("sent.txt") else set()

    # Folder download karega
    gdown.download_folder(url=FOLDER_LINK, quiet=True, use_cookies=False)
    
    files = [f for f in glob.glob("**/*", recursive=True) if os.path.isfile(f) and os.path.getsize(f) > 0]

    async with TelegramClient(StringSession(STRING), API_ID, API_HASH) as client:
        for filepath in files:
            fname = os.path.basename(filepath)
            if fname in sent or fname in ["main.py", "requirements.txt"]: 
                continue
            print(f"Sending {fname}")
            await client.send_file(CHAT_ID, filepath, caption=fname)
            open("sent.txt","a").write(fname+"\n")

asyncio.run(main())
