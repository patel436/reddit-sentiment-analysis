from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio


class RedditCommentsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("broadcast_group", self.channel_name)
        await self.send(text_data=json.dumps({'message': 'Your message here'}))
        print("I connect with you")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("broadcast_group", self.channel_name)

    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=json.dumps({'message': 'Your message here'}))

        await asyncio.sleep(0.00000001)
        # Optional: Handle data sent from the client (if needed)
        pass

    async def send_message(self, message):
        # This method is used to send messages to the WebSocket client.
        # The 'event' parameter will contain the data to be sent.
        if message is not None:
            # Send the message to the WebSocket client
            await self.send(text_data=json.dumps({
                'message': message
            }))

