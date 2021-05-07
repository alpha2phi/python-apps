import React, { Suspense } from "react";
import { ThemeProvider } from "styled-components";
import Loader from "./components/Loader";
import Viewer from "./components/Viewer";
import theme from "./theme/Theme";
import "./App.css";
import config from "./config/config";
import { ApolloProvider } from '@apollo/client/react';
import { split, HttpLink, ApolloClient, InMemoryCache } from '@apollo/client';
import { getMainDefinition } from '@apollo/client/utilities';
import { WebSocketLink } from '@apollo/client/link/ws';

const wsLink = new WebSocketLink({
	uri: `${config.WS_SERVER}`,
	options: {
		reconnect: true
	}
});

const httpLink = new HttpLink({
	uri: `${config.HTTP_SERVER}`
});

const splitLink = split(
	({ query }) => {
		const definition = getMainDefinition(query);
		return (
			definition.kind === 'OperationDefinition' &&
			definition.operation === 'subscription'
		);
	},
	wsLink,
	httpLink,
);

const client = new ApolloClient({
	link: splitLink,
	cache: new InMemoryCache()
});

function Page() {
	return (
		<ThemeProvider theme={theme}>
			<div className="App">
				<h1>Serving ML Model using GraphQL</h1>
				<Viewer />
			</div>
		</ThemeProvider>
	);
}

function App() {
	return (
		<Suspense fallback={<Loader />}>
			<ApolloProvider client={client}>
				<Page />
			</ApolloProvider>
		</Suspense>
	);
}
export default App;
