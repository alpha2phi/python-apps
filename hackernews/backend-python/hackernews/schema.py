import graphene

import links.schema


class Query(links.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
