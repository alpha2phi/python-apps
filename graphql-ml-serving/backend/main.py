import asyncio
import uvicorn
from fastapi import FastAPI
from ariadne import make_executable_schema, SubscriptionType
from ariadne.asgi import GraphQL

app = FastAPI()

# ariadne copied from https://ariadnegraphql.org/docs/subscriptions
type_def = """
    type Query {
        _unused: Boolean
    }

    type Subscription {
        counter: Int!
    }
"""

subscription = SubscriptionType()


@subscription.source("counter")
async def counter_generator(obj, info):
    for i in range(5):
        await asyncio.sleep(1)
        yield i


@subscription.field("counter")
def counter_resolver(count, info):
    return count + 1


schema = make_executable_schema(type_def, subscription)

app.mount("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088)
