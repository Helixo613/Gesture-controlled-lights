import mediapipe  # Library for hand tracking
import cv2  # OpenCV for image processing
import numpy  # NumPy for mathematical operations
import math  # Math for distance calculation

class Hand:
    def __init__(self, mode=False, maxh=1, complex=1, det_conf=0.9, trac_conf=0.9):
        """
        Initializes the Hand tracking class.

        Parameters:
        - mode: Whether to detect hands in a static image or video stream.
        - maxh: Maximum number of hands to detect.
        - complex: Complexity level of the model (higher means more accuracy).
        - det_conf: Minimum confidence for hand detection.
        - trac_conf: Minimum confidence for hand tracking.
        """
        self.hands = mediapipe.solutions.hands.Hands(mode, maxh, complex, det_conf, trac_conf)
        self.pen = mediapipe.solutions.drawing_utils  # Utility for drawing hand landmarks
        self.results = None  # Stores hand tracking results
        self.line_dist = 0  # Distance between fingers

    def get_hand(self, img):
        """
        Processes the given image to detect hands.

        Parameters:
        - img: Input image from the camera.

        Returns:
        - img: Processed image with detected hands.
        """
        _img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for MediaPipe processing
        self.results = self.hands.process(_img)  # Detect hands in the image

        # Uncomment to draw landmarks on detected hands
        # if self.results.multi_hand_landmarks:
        #     for i in self.results.multi_hand_landmarks:
        #         self.pen.draw_landmarks(img, i, mediapipe.solutions.hands.HAND_CONNECTIONS)

        return img

    def get_finger(self, img, finger=""):
        """
        Retrieves the landmarks (coordinates) for a specified finger.

        Parameters:
        - img: Input image.
        - finger: The name of the finger to track (default is all fingers).

        Returns:
        - List of coordinates for the given finger.
        """
        positions = []

        # Assigning landmark indexes for each finger
        if finger == "thumb":
            points = [2, 3, 4]
        elif finger == "index":
            points = [5, 6, 7, 8]
        elif finger == "middle":
            points = [9, 10, 11, 12]
        elif finger == "ring":
            points = [13, 14, 15, 16]
        elif finger == "pinky":
            points = [17, 18, 19, 20]
        else:
            # Return positions of all fingers if no specific finger is mentioned
            return [
                self.get_finger(img, "thumb"),
                self.get_finger(img, "index"),
                self.get_finger(img, "middle"),
                self.get_finger(img, "ring"),
                self.get_finger(img, "pinky")
            ]

        if not self.results:
            self.get_hand(img)  # Process the image to detect hands

        if self.results.multi_hand_landmarks:
            h, w = img.shape[:2]  # Get image dimensions
            for i in self.results.multi_hand_landmarks:
                for point, landmark in enumerate(i.landmark):
                    if point in points:
                        positions.append((int(landmark.x * w), int(landmark.y * h)))  # Convert relative coords to absolute

        return positions if positions else None  # Return positions or None if no finger is detected

    def finger_count(self, img):
        """
        Counts the number of fingers extended based on landmark positions.

        Parameters:
        - img: Input image.

        Returns:
        - String representing the number of fingers extended.
        """
        mapping = {0: "ZERO", 1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE"}
        count = 0

        points = self.get_finger(img)  # Get all fingers' positions

        if points:
            # Checking if each finger is extended by comparing fingertip position with previous joint
            if points[1][-1][0] > points[1][-2][0]:  # Index finger
                count += 1
            if points[2][-1][0] > points[2][-2][0]:  # Middle finger
                count += 1
            if points[3][-1][0] > points[3][-2][0]:  # Ring finger
                count += 1
            if points[4][-1][0] > points[4][-2][0]:  # Pinky finger
                count += 1
            if points[0][-1][0] > points[0][-2][0]:  # Thumb
                count += 1

        return mapping[count]  # Return the finger count as a string

    def draw_line(self, img, finger1="thumb", finger2="index", draw=False):
        """
        Draws a line between two specified fingers and calculates the distance.

        Parameters:
        - img: Input image.
        - finger1: Name of the first finger.
        - finger2: Name of the second finger.
        - draw: Boolean, if True, draws the line on the image.

        Returns:
        - Tuple containing positions of both fingers and distance between them.
        """
        if not self.results:
            self.get_hand(img)  # Process image if hand tracking results are not available

        if self.results.multi_hand_landmarks:
            for i in self.results.multi_hand_landmarks:
                fing1_pos = self.get_finger(img, finger1)[-1] if self.get_finger(img, finger1) else None
                fing2_pos = self.get_finger(img, finger2)[-1] if self.get_finger(img, finger2) else None

                if fing1_pos and fing2_pos:
                    self.line_dist = math.hypot(fing1_pos[0] - fing2_pos[0], fing1_pos[1] - fing2_pos[1])  # Calculate Euclidean distance

                    if draw:
                        cv2.line(img, fing1_pos, fing2_pos, (0, 255, 0), 5)  # Draw a green line
                        return img

                    return [
                        fing1_pos,
                        ((fing1_pos[0] + fing2_pos[0]) // 2, (fing1_pos[1] + fing2_pos[1]) // 2),
                        fing2_pos
                    ], self.line_dist  # Return finger positions and distance

        return None, None  # Return None if no fingers are detected

def map_distance_to_scale(distance, min_distance=15, max_distance=200):
    """
    Maps a measured distance to a scale of 0 to 5.

    Parameters:
    - distance: The measured distance between fingers.
    - min_distance: Minimum distance for scaling.
    - max_distance: Maximum distance for scaling.

    Returns:
    - String representation of the mapped value.
    """
    mapping = {0: "ZERO", 1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE"}
    return mapping[int(numpy.interp(distance, [min_distance, max_distance], [0, 5]))]  # Scale and map the value

if __name__ == "__main__":
    camera = cv2.VideoCapture(0)  # Open camera feed
    detector = Hand()  # Initialize hand tracking

    while True:
        _, img = camera.read()  # Capture frame from camera
        detector.get_hand(img)  # Process the frame for hand tracking
        detector.draw_line(img, draw=True)  # Draw a line between thumb and index finger

        # Print the mapped finger distance
        print(map_distance_to_scale(detector.line_dist))

        cv2.imshow("Camera", img)  # Display the camera feed
        cv2.waitKey(1)  # Wait for a key press (loop continues indefinitely)
