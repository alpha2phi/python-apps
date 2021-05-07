from ariadne import QueryType, convert_kwargs_to_snake_case
from config import messages, clients

query = QueryType()


@query.field("messages")
@convert_kwargs_to_snake_case
async def resolve_messages(obj, info, client_id):
    def filter_by_client_id(message):
        return message["client_id"] == client_id

    client_messages = filter(filter_by_client_id, messages)
    return {"success": True, "messages": client_messages}


@query.field("clientId")
@convert_kwargs_to_snake_case
async def resolve_user_id(obj, info, client_id):
    client = clients.get(client_id)
    if client:
        return client["client_id"]
