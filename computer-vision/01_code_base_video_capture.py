import time
import cv2


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

    try:

        pTime = time.time()
        while cap.isOpened():
            # Read from video capture device
            success, img = cap.read()

            # FPS
            pTime, img = calculate_fps(img, pTime)

            # Show video
            if img is not None:
                cv2.imshow("Video", img)

            # Wait for key to exit
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    show_video("computer-vision/dancing.mp4")
