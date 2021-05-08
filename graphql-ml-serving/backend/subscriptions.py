import logging
import base64
import json
import io
from ariadne import convert_kwargs_to_snake_case, SubscriptionType
from config import queue
from model import photo_2_cartoon

subscription = SubscriptionType()


@subscription.source("messages")
@convert_kwargs_to_snake_case
async def messages_source(obj, info, client_id):
    while True:
        message = await queue.get()

        logging.info(f"generating -- {client_id} - {message['client_id']}")

        if message["client_id"] == client_id:
            logging.info(f"message['content']")
            raw_data = json.loads(message['content'])
            data = raw_data["data"]
            bytes_data = base64.b64decode(data)

            # cartoon_image = photo_2_cartoon(bytes_data)
            # bytes_io = io.BytesIO()
            # cartoon_image.save(bytes_io, format="PNG")

            queue.task_done()
            yield message
        else:
            queue.put(message)


@subscription.field("messages")
@convert_kwargs_to_snake_case
async def messages_resolver(message, info, client_id):
    logging.info(f"sending --- {len(message['content'])}")
    return message
