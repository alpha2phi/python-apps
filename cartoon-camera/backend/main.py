import base64
from io import BytesIO
import json
import logging
import sys
from typing import List
import uuid
from PIL import Image
from starlette.responses import Response
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
import uvicorn

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from cartoon import cartoonify

# FastAPI
app = FastAPI(
    title="Cartoon Camera",
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
    encoded_img = "data:image/png;base64," + base64.b64encode(
        img_byte).decode()
    return encoded_img


def process_incoming_request(payload):
    parsed_data = json.loads(payload)
    data = parsed_data["data"]
    style = parsed_data["style"]

    # Convert to PIL image
    image = data[data.find(",") + 1:]
    dec = base64.b64decode(image + "===")
    image = Image.open(BytesIO(dec))

    # Process the image
    cartoon_img = cartoonify(image, style)

    result = {
        "output": base64_encode_img(cartoon_img),
    }
    return result


@app.get("/")
def home():
    return {"message": "Cartoon Camera"}


@app.post("/cartoon")
def process_cartoon(file: UploadFile = File(...), style=0, load_size=450):
    """
    Transform uploaded image file into cartoon image.

    :param file UploadFile: Uploaded image.
    :param style int: Style to applic (0 - Hayao, 1 - Hosoda, 2 - Paprika, 3 - Shinkai).
    :param load_size int: Default to 450.
    """
    file_bytes = file.file.read()
    image = Image.open(BytesIO(file_bytes))
    output_image = cartoonify(image, style, load_size)
    bytes_io = BytesIO()
    output_image.save(bytes_io, format="PNG")
    return Response(bytes_io.getvalue(), media_type="image/png")


@app.websocket("/cartoon_ws/{client_id}")
async def process_cartoon_ws(websocket: WebSocket, client_id: int):
    await conn_mgr.connect(websocket)
    try:
        while True:
            received = await websocket.receive_text()

            # Process request
            result = process_incoming_request(received)

            # Send back the result
            await conn_mgr.send_message(json.dumps(result), websocket)

    except WebSocketDisconnect:
        conn_mgr.disconnect(websocket)
        await conn_mgr.broadcast(f"Client #{client_id} left the chat")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
