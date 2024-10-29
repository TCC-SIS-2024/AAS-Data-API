from socketio import AsyncNamespace

class WebsocketNamespace(AsyncNamespace):

    async def on_connect(self, sid, environ):
        print(f"Websocket client connected with sid: {sid}")

    async def on_disconnect(self, sid):
        print(f"Websocket client disconnected: {sid}")

    async def on_sensor_data_esp_32(self, sid, data):
        await self.emit("sensor_data", data)