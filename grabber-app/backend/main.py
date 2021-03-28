import sys
import logging
import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
import uvicorn

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name


app = FastAPI(
    title="Grabber App",
    description="""Visit port 8088/docs for the Swagger documentation.""",
    version="0.0.1",
)

app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
