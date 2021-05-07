import logging
from ariadne import convert_kwargs_to_snake_case, SubscriptionType
from config import queue

subscription = SubscriptionType()


@subscription.source("messages")
@convert_kwargs_to_snake_case
async def messages_source(obj, info, client_id):
    while True:
        message = await queue.get()
        if message["client_id"] == client_id:
            queue.task_done()
            yield message
        else:
            queue.put(message)


@subscription.field("messages")
@convert_kwargs_to_snake_case
async def messages_resolver(message, info, client_id):
    return message
