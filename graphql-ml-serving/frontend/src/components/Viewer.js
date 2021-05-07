import React, { useEffect, useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import styled from "styled-components";
import { gql, useMutation } from '@apollo/client';

const Wrapper = styled.div`
  display: block;
  margin: 0 auto;
`;


export default function Viewer() {
	const webcamRef = useRef(null);
	const [img, setImg] = useState(null);
	const [isPaused, setPause] = useState(false);
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
	const [createMessage, { data }] = useMutation(CREATE_MESSAGE);

	const CapturePhoto = (message) => {
		const {loading, error, data} = createMessage({ variables: { clientId: clientId, content: message} });

		if (loading) console.log("Sending...");
		if (error) console.log("Error sending message..");

		return (
			<p>
				<button onClick={capture}>Capture photo</button>
			</p>
		)
	}

	useEffect(() => {
		setPause(false);

	}, []);

	const videoConstraints = {
		width: 1280,
		height: 720,
		facingMode: "environment", // Can be "environment" or "user"
		screenshotQuality: 1,
	};

	const capture = useCallback(() => {
		const capturedImg = webcamRef.current.getScreenshot();
		const data = JSON.stringify({ data: capturedImg });
		// SendMessage(data);
	}, [webcamRef]);

	return (

		<Wrapper>
			<Webcam
				audio={false}
				ref={webcamRef}
				screenshotFormat="image/jpeg"
				width="50%"
				videoConstraints={videoConstraints}
			/>


			{img && <img alt="Cartoon" src={img} width="50%" />}


		</Wrapper>
	);
}
