import logging
import asyncio
from ariadne import convert_kwargs_to_snake_case, SubscriptionType

subscription = SubscriptionType()


@subscription.source("messages")
@convert_kwargs_to_snake_case
async def messages_generator(obj, info, client_id, data):
    while True:
        logging.info("source")
        await asyncio.sleep(1)
        message = {
            "content": data,
            "sender_id": client_id,
            "recipient_id": "afdsf"
        }
        yield message


@subscription.field("messages")
@convert_kwargs_to_snake_case
async def messages_resolver(message, info, client_id, data):
    logging.info("resolver")
    return message


@subscription.source("counter")
async def counter_generator(obj, info):
    for i in range(5):
        logging.info("generating.......")
        await asyncio.sleep(1)
        yield i


@subscription.field("counter")
def counter_resolver(count, info):
    return count + 1
