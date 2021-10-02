import time
import cv2
import mediapipe as mp


def calculate_fps(img, pTime, pos=(50, 80), color=(0, 255, 0), scale=4, thickness=4):
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(
        img,
        f"FPS: {int(fps)}",
        pos,
        cv2.FONT_HERSHEY_PLAIN,
        scale,
        color,
        thickness,
    )
    return pTime, img


def show_video(capture):
    # cap = cv2.VideoCapture(0) # Capture from camera. Adjust the number
    cap = cv2.VideoCapture(capture)  # Capture from video

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    try:
        pTime = time.time()

        with mp_hands.Hands(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as hands:

            while cap.isOpened():
                # Read from video capture device
                success, img = cap.read()

                # FPS
                pTime, img = calculate_fps(img, pTime)

                # Convert from BGR to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # To improve performance, optionally mark the image as not writeable to pass by reference.
                img.flags.writeable = False
                results = hands.process(img)

                # Draw the hand annotations on the image.
                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            img,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style(),
                        )

                # Show video
                if img is not None:
                    cv2.imshow("Hands", img)

                # Wait for key to exit
                if cv2.waitKey(10) & 0xFF == ord("q"):
                    break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    show_video("computer-vision/hands.mp4")
