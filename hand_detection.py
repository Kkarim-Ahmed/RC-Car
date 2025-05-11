
import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Function to determine hand state (open/closed) and which fingers are up
def get_hand_state(landmarks):
    if not landmarks or len(landmarks) < 21:
        return False, False, []

    # Thumb (tip 4, joint 3)
    thumb_up = landmarks[4].x < landmarks[3].x if landmarks[4].x else False

    # Four fingers (compare tip to lower joint)
    fingers_up = [
        landmarks[8].y < landmarks[6].y,  # Index
        landmarks[12].y < landmarks[10].y,  # Middle
        landmarks[16].y < landmarks[14].y,  # Ring
        landmarks[20].y < landmarks[18].y,  # Pinky
    ]

    # Count raised fingers
    raised_fingers = fingers_up.count(True) + int(thumb_up)

    # Determine if hand is closed or open
    hand_closed = raised_fingers == 0
    hand_open = raised_fingers == 5

    return hand_closed, hand_open, fingers_up

# Open webcam
cap = cv2.VideoCapture(0)

with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip image horizontally for a mirror effect
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        # Check for hands
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get hand state
                hand_closed, hand_open, fingers_up = get_hand_state(hand_landmarks.landmark)

                # Display status on screen
                text = f"Open: {hand_open}, Closed: {hand_closed}, Fingers Up: {fingers_up.count(True)}"
                cv2.putText(image, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Display the processed image
        cv2.imshow('Hand Detection', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
