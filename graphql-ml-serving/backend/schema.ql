schema {
	query: Query
	subscription: Subscription
}

type Message {
    content: String
}

type Query {
	hello: String!
}

type Subscription {
	messages(clientId: String, data: String): Message
	counter: Int!
}
