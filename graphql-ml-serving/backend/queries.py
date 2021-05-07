from ariadne import QueryType

query = QueryType()


@query.field("hello")
def resolve_hello(*_):
    return "Hello world!"
