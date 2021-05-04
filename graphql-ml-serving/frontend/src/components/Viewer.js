import React, { useEffect, useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import styled from "styled-components";
import config from "../config/config";
import { useFormFields } from "../libs/hooksLib";

const Wrapper = styled.div`
  display: block;
  margin: 0 auto;
`;

const Select = styled.select`
  width: 30%;
  height: 40px;
  background: lightgray;
  color: black;
  padding-left: 5px;
  font-size: 14px;
  border: none;
  margin-left: 10px;
  margin-bottom: 30px;

  option {
    color: black;
    background: lightgray;
    display: flex;
    white-space: pre;
    min-height: 20px;
    padding: 0px 2px 1px;
  }
`;

export default function Viewer() {
  const [fields, handleFieldChange] = useFormFields({
    style: "2",
  });
  const webcamRef = useRef(null);
  const [cartoonImg, setCartoonImg] = useState(null);

  const [isPaused, setPause] = useState(false);
  const ws = useRef(null);

  useEffect(() => {
    setPause(false);
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
      const message = JSON.parse(event.data);
      setCartoonImg(message.output);
      console.log(message);
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
    screenshotQuality: 1,
  };

  const capture = useCallback(() => {
    const capturedImg = webcamRef.current.getScreenshot();

    const data = JSON.stringify({ data: capturedImg, style: fields.style });
    sendMessage(data);
  }, [webcamRef, fields]);

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
        Select Style:
        <Select id="style" onChange={handleFieldChange} value={fields.style}>
          <option value="0">Hayao</option>
          <option value="1">Hosoda</option>
          <option value="2">Paprika</option>
          <option value="3">Shinkai</option>
        </Select>
        <br />
        <button onClick={capture}>Capture photo</button>
      </p>
      {cartoonImg && <img alt="Cartoon" src={cartoonImg} width="50%" />}
    </Wrapper>
  );
}
