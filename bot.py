import os
import json
import discord
import datetime
from scam_detection import ScamDetector

class ScamDetectorBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)

        with open("config.json", "r") as config_file:
            config = json.load(config_file)

        self.punishment_type: str = config["punishment_type"].lower()
        self.detector = ScamDetector("config.json")

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or not message.attachments:
            return

        for attachment in message.attachments:
            if not attachment.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            image_bytes = await attachment.read()
            if self.detector.is_scam(image_bytes):
                print(f"Match found: {attachment.filename} from {message.author}")
                await self.punish_message(message)
                return

    async def punish_message(self, message: discord.Message) -> None:
        await message.delete()
        author = message.author
        if not message.guild or not isinstance(author, discord.Member):
            return 

        if self.punishment_type == "timeout":
            await author.timeout(datetime.datetime.now() + datetime.timedelta(minutes=10), reason="Sent flagged scam image")
        elif self.punishment_type == "kick":
            await message.guild.kick(author, reason="Sent flagged scam image")
        elif self.punishment_type == "ban":
            await message.guild.ban(author, reason="Sent flagged scam image")
            
if __name__ == "__main__":
    ScamDetectorBot().run(os.environ["DISCORD_BOT_TOKEN"])
