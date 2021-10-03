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
    mp_face_mesh = mp.solutions.face_mesh
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    try:
        pTime = time.time()

        with mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as face_mesh:

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

                results = face_mesh.process(img)

                # Draw the hand annotations on the image.
                img.flags.writeable = True
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        mp_drawing.draw_landmarks(
                            image=img,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
                        )
                        mp_drawing.draw_landmarks(
                            image=img,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style(),
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
