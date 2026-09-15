import os, asyncio, glob
from telethon import TelegramClient
from telethon.sessions import StringSession
import gdown

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING = os.environ.get("STRING")
CHAT_ID = int(os.environ.get("CHAT_ID"))
FOLDER_LINK = "https://drive.google.com/drive/folders/14pY4V62ImG6g6XpkPFD2Y6IJDX9SlNKM?usp=drive_link"

async def main():
    sent = open("sent.txt").read().splitlines() if os.path.exists("sent.txt") else []
    sent = set(sent)

    # Folder list karo, download ek-ek karke, fail hua toh skip
    try:
        gdown.download_folder(url=FOLDER_LINK, quiet=True, use_cookies=False)
    except:
        pass # error ko ignore kar

    all_files = glob.glob("Tg/**/*", recursive=True)

    async with TelegramClient(StringSession(STRING), API_ID, API_HASH) as client:
        for path in all_files:
            if not os.path.isfile(path): continue
            name = os.path.basename(path)
            if name in sent: continue
            if os.path.getsize(path) < 1000: continue # khali file skip

            try:
                await client.send_file(CHAT_ID, path, caption=name)
                open("sent.txt","a").write(name+"\n")
                print(f"Done {name}")
            except Exception as e:
                print(f"Skip {name}: {e}")
                continue

asyncio.run(main())
