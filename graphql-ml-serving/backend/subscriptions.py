import logging
import base64
from io import BytesIO
from ariadne import convert_kwargs_to_snake_case, SubscriptionType
from config import queue
from model import photo_2_cartoon, base64_encode_img

subscription = SubscriptionType()


@subscription.source("messages")
@convert_kwargs_to_snake_case
async def messages_source(obj, info, client_id):
    while True:
        message = await queue.get()
        if message["client_id"] == client_id:
            logging.info("Processing...")
            content = message['content']
            decoded = content[content.find(",") + 1:]
            bytes_data = BytesIO(base64.b64decode(decoded + "==="))
            cartoon_image = photo_2_cartoon(bytes_data)
            bytes_io = BytesIO()
            cartoon_image.save(bytes_io, format="PNG")
            message['content'] = base64_encode_img(cartoon_image)
            queue.task_done()
            logging.info("Done...")
            yield message
        else:
            await queue.put(message)


@subscription.field("messages")
@convert_kwargs_to_snake_case
async def messages_resolver(message, info, client_id):
    logging.info(f"Sending result - {len(message['content'])}")
    return message
