name = "hunt bot"
import time
class auto:
    def __init__(self, client, channelid: int, seconds: int):
        self.client = client
        self.channel = client.get_channel(channelid)
        self.seconds = seconds
        self.update = time.time()
    async def run(self):
        if time.time() - self.update >= self.seconds:
            self.update = time.time()
            await self.client.send_message(self.channel, "owo hunt")