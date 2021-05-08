import React, { useEffect, useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import styled from "styled-components";
import { gql, useMutation, useSubscription } from '@apollo/client';

const Wrapper = styled.div`
  display: block;
  margin: 0 auto;
`;

const clientId = Date.now().toString();

const CREATE_MESSAGE = gql`
mutation createMessage($clientId: String!, $content: String!) {
	createMessage(clientId: $clientId, content: $content) {
		message {
			content
		}
		success
		errors
	}
}
`;

const REGISTER_CLIENT = gql`
mutation createClient($clientId: String!) {
	createClient(clientId: $clientId) {
		client {
			clientId
		}
		success
		errors
	}
}
`;

const RECEIVE_MESSAGE = gql`
subscription messages($clientId: String!) {
	messages(clientId: $clientId) {
		content
		clientId
	}
}
`;

const ReceiveMessage = () => {
	const { data, loading, error } = useSubscription(RECEIVE_MESSAGE, { variables: { clientId: clientId } });

	if (loading) {
		return "";
	}
	if (error) {
		console.error(error);
		return <h4>Error processing</h4>;
	}
	var content = "";
	if (data) {
		content = data.messages.content;
	}
	console.log("recieve----", content.length);
	return <img alt="result" src={content} width={"50%"}/>
}

export default function Viewer() {
	const webcamRef = useRef(null);
	const [status, setStatus] = useState("Status");

	const videoConstraints = {
		width: 1280,
		height: 720,
		facingMode: "environment", // Can be "environment" or "user"
		screenshotQuality: 1,
	};

	const [createMessage] = useMutation(CREATE_MESSAGE, {
		onError: (err) => console.error(err),
		onCompleted: () => setStatus("Request sent")
	});

	const capture = useCallback(() => {
		const capturedImg = webcamRef.current.getScreenshot();
		const data = JSON.stringify({ data: capturedImg });
		console.log('sending ----');
		createMessage({ variables: { clientId: clientId, content: data } });
	}, [webcamRef, createMessage]);


	const [registerClient] = useMutation(REGISTER_CLIENT, {
		onError: (err) => console.error(err),
		onCompleted: (result) => setStatus(`Registered with ${result.createClient.client.clientId}`)
	});
	useEffect(() => {
		registerClient({ variables: { clientId: clientId } });
	}, [registerClient]);



	return (

		<Wrapper>
			<Webcam
				audio={false}
				ref={webcamRef}
				screenshotFormat="image/jpeg"
				width="50%"
				videoConstraints={videoConstraints}
			/>

			<h3>{status}</h3>
			<p>
				<button onClick={capture}>Capture photo</button>
			</p>
			<ReceiveMessage />
		</Wrapper>
	);
}
