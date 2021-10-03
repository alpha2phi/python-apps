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
    mp_holistic = mp.solutions.holistic

    try:
        pTime = time.time()

        with mp_holistic.Holistic(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as holistic:

            while cap.isOpened():
                # Read from video capture device
                success, img = cap.read()
                if not success:
                    continue

                # FPS
                pTime, img = calculate_fps(img, pTime)

                # Convert from BGR to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # To improve performance, optionally mark the image as not writeable to pass by reference.
                img.flags.writeable = False

                results = holistic.process(img)

                # Draw the hand annotations on the image.
                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                mp_drawing.draw_landmarks(
                    img,
                    results.face_landmarks,
                    mp_holistic.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style(),
                )
                mp_drawing.draw_landmarks(
                    img,
                    results.pose_landmarks,
                    mp_holistic.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
                )

                mp_drawing.draw_landmarks(
                    img,
                    results.right_hand_landmarks,
                    mp_holistic.HAND_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                    connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style(),
                )

                mp_drawing.draw_landmarks(
                    img,
                    results.left_hand_landmarks,
                    mp_holistic.HAND_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                    connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style(),
                )

                # Show video
                if img is not None:
                    cv2.imshow("Face mesh", img)

                # Wait for key to exit
                if cv2.waitKey(10) & 0xFF == ord("q"):
                    break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    show_video("computer-vision/dancing.mp4")
