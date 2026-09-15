import os, asyncio, glob
from telethon import TelegramClient
from telethon.sessions import StringSession
import gdown

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
STRING = os.environ.get("STRING")
CHAT_ID = int(os.environ.get("CHAT_ID"))

FOLDER_LINK = "https://drive.google.com/drive/folders/16lFzZGq9s-4ExvK72-8Y9-FUgbcPBG38?usp=drive_link"

async def main():
    if not os.path.exists("sent.txt"):
        open("sent.txt","w").close()
    sent = set(open("sent.txt").read().splitlines())

    print("Downloading folder...")
    try:
        gdown.download_folder(url=FOLDER_LINK, quiet=False, use_cookies=False)
    except Exception as e:
        print(f"Download me kuch files fail hui, but chalta hai: {e}")

    files = glob.glob("**/*", recursive=True)
    
    async with TelegramClient(StringSession(STRING), API_ID, API_HASH) as client:
        for f in files:
            if not os.path.isfile(f): continue
            if "my-dumb-bin" in f or f in ["main.py","requirements.txt","sent.txt"]: continue
            name = os.path.basename(f)
            if name in sent or os.path.getsize(f) < 500: continue
            
            try:
                print(f"Sending {name}")
                await client.send_file(CHAT_ID, f, caption=name)
                open("sent.txt","a").write(name+"\n")
            except Exception as e:
                print(f"Failed {name}: {e}")

asyncio.run(main())
