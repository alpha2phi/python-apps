import base64
import io
import json
import logging
import sys
import uuid
from io import BytesIO
from typing import List

import uvicorn
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from model import yolov5
from PIL import Image
from starlette.responses import Response

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# FastAPI
app = FastAPI(
    title="Serving YOLO",
    description="""Visit port 8088/docs for the FastAPI documentation.""",
    version="0.0.1",
)


class ConnectionManager:
    """Web socket connection manager."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


conn_mgr = ConnectionManager()


def base64_encode_img(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    img_byte = buffered.getvalue()
    encoded_img = "data:image/png;base64," + base64.b64encode(img_byte).decode()
    return encoded_img


@app.get("/")
def home():
    return {"message": "YOLO - You Only Look Once"}


@app.post("/yolo")
def process_yolov5(file: UploadFile = File(...)):
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    name = f"/data/{str(uuid.uuid4())}.png"

    # image.save(name)
    image.filename = name
    classes, converted_img = yolov5(image)

    bytes_io = io.BytesIO()
    converted_img.save(name)
    converted_img.save(bytes_io, format="PNG")
    return Response(bytes_io.getvalue(), media_type="image/png")


@app.websocket("/yolo_ws/{client_id}")
async def process_yolov5_ws(websocket: WebSocket, client_id: int):
    await conn_mgr.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            # Convert to PIL image
            image = data[data.find(",") + 1:]
            dec = base64.b64decode(image + "===")
            image = Image.open(BytesIO(dec)).convert("RGB")

            # Process the image
            name = f"/data/{str(uuid.uuid4())}.png"
            image.filename = name
            classes, converted_img = yolov5(image)

            result = {
                "prediction": json.dumps(classes),
                "output": base64_encode_img(converted_img),
            }
            # logging.info("-----", json.dumps(result))

            # Send back the result
            await conn_mgr.send_message(json.dumps(result), websocket)

            # await conn_mgr.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        conn_mgr.disconnect(websocket)
        await conn_mgr.broadcast(f"Client #{client_id} left the chat")


ws_client_html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8088/yolo_ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/yolo_client")
async def process_yolo_client():
    return HTMLResponse(ws_client_html)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
