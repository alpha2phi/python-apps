import React, { useEffect, useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import styled from "styled-components";
import { gql, useMutation } from '@apollo/client';
import ImageViewer from "./ImageViewer";

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
		createMessage({ variables: { clientId: clientId, content: capturedImg } });
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
			<ImageViewer clientId={clientId} />
		</Wrapper>
	);
}
