import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

import uvicorn
from fastapi import FastAPI
from ariadne.asgi import GraphQL
from ariadne import make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL
from queries import query
from subscriptions import subscription

app = FastAPI()

type_defs = load_schema_from_path("schema.ql")

schema = make_executable_schema(type_defs, query, subscription,
                                snake_case_fallback_resolvers)
# app.add_route("/graphql", GraphQL(schema, debug=True))
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088)

# https://ariadnegraphql.org/docs/subscriptions
# https://www.twilio.com/blog/graphql-api-subscriptions-python-asyncio-ariadne
# https://github.com/mrkiura/chat_api_subscriptions
# https://www.twilio.com/blog/graphql-api-python-flask-ariadne
