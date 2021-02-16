import React, { useEffect, useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import styled from "styled-components";
import config from "./config/config";

const Wrapper = styled.div`
  display: block;
  margin: 0 auto;
`;

export default function Viewer() {
  useEffect(() => {
    onLoad();
  }, []);

  async function onLoad() {
    console.log(config.WS_SERVER);
  }

  const webcamRef = useRef(null);
  const [capturedImg, setCapturedImg] = useState(null);

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "environment", // Can be "environment" or "user"
  };

  const capture = useCallback(() => {
    const capturedImg = webcamRef.current.getScreenshot();
    // console.log(capturedImg);
    setCapturedImg(capturedImg);
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
