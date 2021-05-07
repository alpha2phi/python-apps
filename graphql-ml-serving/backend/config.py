import asyncio

messages = []
clients = {}

queue = asyncio.Queue()


def create_client(client_id):
    if not clients.get(client_id):
        client = {"client_id": client_id}
        clients[client_id] = client
        return {"success": True, "client": client}
