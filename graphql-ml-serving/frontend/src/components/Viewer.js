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
	const clientId = Date.now();

	const CREATE_MESSAGE = gql`
		mutation {
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

	useEffect(() => {
		setPause(false);

		createMessage({ variables: { clientId: clientId, content: "from web app"} })
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

			<p>
				<button onClick={capture}>Capture photo</button>
			</p>

			{img && <img alt="Cartoon" src={img} width="50%" />}

		</Wrapper>
	);
}
