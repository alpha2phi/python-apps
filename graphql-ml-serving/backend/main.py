import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

import uvicorn
# from fastapi import FastAPI
from ariadne.asgi import GraphQL
from ariadne import make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers
from ariadne.asgi import GraphQL
from queries import query
from mutations import mutation
from subscriptions import subscription

# app = FastAPI()
# sub_app = FastAPI()

type_defs = load_schema_from_path("schema.ql")

schema = make_executable_schema(type_defs, query, mutation, subscription,
                                snake_case_fallback_resolvers)

app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088)

# sub_app.add_route("/", GraphQL(schema, debug=True))
# app.mount("/graphql", sub_app)
# app.add_route("/graphql", GraphQL(schema, debug=True))

# https://ariadnegraphql.org/docs/subscriptions
# https://www.twilio.com/blog/graphql-api-subscriptions-python-asyncio-ariadne
# https://github.com/mrkiura/chat_api_subscriptions
# https://www.twilio.com/blog/graphql-api-python-flask-ariadne
