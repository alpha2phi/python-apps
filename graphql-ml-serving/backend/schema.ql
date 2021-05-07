schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}

type Query {
    messages(clientId: String!): messagesResult
    clientId(clientId: String!): String
}

type Message {
    content: String
    clientId: String
}

type Client {
    clientId: String
}

type createClientResult {
    client: Client
    success: Boolean!
    errors: [String]
}

type createMessageResult {
    message: Message
    success: Boolean!
    errors: [String]
}

type messagesResult {
    messages: [Message]
    success: Boolean!
    errors: [String]
}

type Mutation {
    createMessage(clientId: String, content: String): createMessageResult
    createClient(clientId: String!): createClientResult
}

type Subscription {
    messages(clientId: String): Message
}
