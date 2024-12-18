import cv2
import numpy as np
import handDetectionModule as htm
import math
import asyncio
import aiohttp
import threading

async def send_volume_to_api_async(vol):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:8000/update-value", json={"value": vol}) as response:
                if response.status == 200:
                    print(f"Volume sent successfully: {vol}")
                else:
                    print(f"Failed to send volume: {response.status}")
    except Exception as e:
        print(f"Error sending volume to API: {e}")


def async_send_volume(vol):
    loop = asyncio.new_event_loop()  # Create a new event loop for each thread
    asyncio.set_event_loop(loop)  # Set the event loop for the thread
    loop.run_until_complete(send_volume_to_api_async(vol))

def main():
    # Turn on the camera (0) and start capture
    video = cv2.VideoCapture(0)
    # Setting the captured video's dimensions
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 720p width = 1280 pixels
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 720p height = 720 pixels
    video.set(cv2.CAP_PROP_FPS, 30)            # Force 30 FPS

    detect = htm.handDetector()  # Make an object for hand detection module

    while True:
        check, frame = video.read()  # Check & capture the frame
        # Flip the frame for a mirror image like o/p
        frame = cv2.flip(frame, 1)
        # Get landmarks & store in a list
        LmarkList = detect.findPosition(frame, draw=False)
        if len(LmarkList) != 0:
            print(LmarkList[4], LmarkList[8])

            # Coordinates for landmarks of Thumb & Index fingers
            x1, y1 = LmarkList[4][1], LmarkList[4][2]
            x2, y2 = LmarkList[8][1], LmarkList[8][2]

            cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)  # Draw circle @ thumb tip
            cv2.circle(frame, (x2, y2), 15, (0, 255, 0), cv2.FILLED)  # Draw circle @ index tip
            cv2.line(frame, (x1, y1), (x2, y2), (7, 0, 212), 3, 5)

            # Midpoint for thumb-index joining line
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Draw circle @ midpoint of the thumb-index joining line
            cv2.circle(frame, (cx, cy), 15, (255, 255, 255), cv2.FILLED)

            # Joining line length
            length = math.hypot(x2 - x1, y2 - y1)

            vol = np.interp(length, [50, 300], [0, 100])
            # Call async API function in a background thread
            threading.Thread(target=async_send_volume, args=(int(vol),)).start()

            # Changing colors for respective lengths of joining line
            if length <= 50:
                cv2.circle(frame, (cx, cy), 15, (0, 0, 255), cv2.FILLED)  
            elif length >= 200:
                cv2.circle(frame, (cx, cy), 15, (250, 0, 0), cv2.FILLED)  # Blue circle

        cv2.putText(frame, "Press 'q' to exit", (25, 450), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 0), 2)  # Display quit key on o/p window
        cv2.imshow('=== Khedmet El Mrammeji ===', frame)  # Open window for showing the o/p

        # Escape key (q)
        if cv2.waitKey(1) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
