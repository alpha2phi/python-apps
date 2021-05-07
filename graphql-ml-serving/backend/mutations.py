import logging
from ariadne import MutationType, convert_kwargs_to_snake_case
from config import clients, messages, queue

mutation = MutationType()


@mutation.field("createMessage")
@convert_kwargs_to_snake_case
async def resolve_create_message(obj, info, content, client_id):
    try:
        logging.info(f"Received from {client_id}: {len(content)}")
        message = {"content": content, "client_id": client_id}
        messages.append(message)
        await queue.put(message)
        return {"success": True, "message": message}
    except Exception as error:
        return {"success": False, "errors": [str(error)]}


@mutation.field("createClient")
@convert_kwargs_to_snake_case
async def resolve_create_client(obj, info, client_id):
    try:
        logging.info(f"Client id: {client_id}")
        if not clients.get(client_id):
            client = {"client_id": client_id}
            clients[client_id] = client
            return {"success": True, "client": client}
        return {"success": False, "errors": ["Client is taken"]}

    except Exception as error:
        return {"success": False, "errors": [str(error)]}
