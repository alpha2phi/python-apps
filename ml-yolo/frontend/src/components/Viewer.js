import React, { useEffect, useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import styled from "styled-components";
import config from "../config/config";

const Wrapper = styled.div`
  display: block;
  margin: 0 auto;
`;

export default function Viewer() {
  const webcamRef = useRef(null);
  const [capturedImg, setCapturedImg] = useState(null);

  const [isPaused, setPause] = useState(false);
  const ws = useRef(null);

  useEffect(() => {
    const client_id = Date.now();
    const url = `${config.WS_SERVER}/${client_id}`;
    console.log(url);
    ws.current = new WebSocket(url);
    ws.current.onopen = () => console.log("ws opened");
    ws.current.onclose = () => console.log("ws closed");

    return () => {
      ws.current.close();
    };
  }, []);

  useEffect(() => {
    if (!ws.current) return;

    ws.current.onmessage = (event) => {
      if (isPaused) return;
      // const message = JSON.parse(e.data);
      // console.log("e", message);
      console.log(event.data);
    };
  }, [isPaused]);

  function sendMessage(msg) {
    if (!ws.current) return;

    ws.current.send(msg);
  }

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "environment", // Can be "environment" or "user"
  };

  const capture = useCallback(() => {
    const capturedImg = webcamRef.current.getScreenshot();
    setCapturedImg(capturedImg);
    // console.log(capturedImg);
    sendMessage(capturedImg);
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
      {capturedImg && <img src={capturedImg} width="50%" />}
    </Wrapper>
  );
}
