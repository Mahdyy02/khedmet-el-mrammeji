"""
    Detect hands using cv2 & mediapipe library
    Draw lines to connect the landmarks of the detected hands
"""
import cv2
import mediapipe as mp


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectConfidence=0.75, trackConfidence=0.75):
        self.mode = mode
        self.maxHands = maxHands
        self.detectConfidence = detectConfidence
        self.trackConfidence = trackConfidence
        self.mpHands = mp.solutions.hands
        # process a RGB image & return the hand landmarks of detected hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        # convert img from BGR to RGB for hands object to process
        rgbImg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(rgbImg)
        if self.result.multi_hand_landmarks:
            for handLmarks in self.result.multi_hand_landmarks:
                if draw:
                    # draw landmarks & connections for them
                    self.mpDraw.draw_landmarks(
                        frame, handLmarks, self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPosition(self, frame, handNo=0, draw=True):
        self.LmarkList = []
        rgbImg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(rgbImg)

        if self.result.multi_hand_landmarks:
            # processed landmarks from Hands() method for 1 hand
            myHand = self.result.multi_hand_landmarks[handNo]
            # get land mark ids
            for LmarkId, lmk in enumerate(myHand.landmark):
                h, w, c = frame.shape  # get o/p window dimension
                # coordinates for landmarks of detected hands
                cx, cy = int(lmk.x * w), int(lmk.y * h)
                self.LmarkList.append([LmarkId, cx, cy])

                if draw:
                    if LmarkId in [4, 8, 12, 16, 20]:  # ids of all finger tips
                        cv2.circle(frame, (cx, cy), 15,
                                   (84, 245, 66), cv2.FILLED)
        return self.LmarkList


def main():
    video = cv2.VideoCapture(0)  # open camera to capture image frame
    detect = handDetector()
    # make o/p window of free dimension
    cv2.namedWindow('=== Live Cam ===', cv2.WINDOW_NORMAL)

    while True:
        check, frame = video.read()  # check & capture the frame
        # flip the frame for a mirror image like o/p
        frame = cv2.flip(frame, 1)
        frame = detect.findHands(frame)
        # get hand landmarks and store in a list
        LmarkList = detect.findPosition(frame)

        cv2.putText(frame, "Press 'Q' to exit", (25, 450), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 0), 2)  # display quit key on o/p window
        # open window for showing the o/p
        cv2.imshow('=== Live Cam ===', frame)

        # escape key (q)
        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == "__main__":
    main()
