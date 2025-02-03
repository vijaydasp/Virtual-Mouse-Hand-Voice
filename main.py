import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import threading
import math
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)

left_click_active = False
right_click_active = False
prev_zoom_distance = None
zoom_threshold = 5
typing_enabled = False

# Variables for double-click detection
last_click_time = 0
double_click_threshold = 0.8  # Time in seconds to detect a double-click

def calculate_distance(landmark1, landmark2, width, height):
    x1, y1 = int(landmark1.x * width), int(landmark1.y * height)
    x2, y2 = int(landmark2.x * width), int(landmark2.y * height)
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def is_finger_up(finger_tip, finger_pip, finger_mcp):
    return finger_tip.y < finger_pip.y < finger_mcp.y

def check_zoom_gesture(hand_landmarks):
    """Check if only index and middle fingers are up"""
    # Get landmarks for all fingers
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    # Check if index and middle are up while others are down
    index_up = is_finger_up(index_tip, index_pip, index_mcp)
    middle_up = is_finger_up(middle_tip, middle_pip, middle_mcp)
    ring_down = ring_tip.y > ring_pip.y
    pinky_down = pinky_tip.y > pinky_pip.y

    return index_up and middle_up and ring_down and pinky_down

def check_scroll_up_gesture(hand_landmarks):
    """Check if only ring finger is up while others are down"""
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    # Check if ring finger is up while others are down
    ring_up = is_finger_up(ring_tip, ring_pip, ring_mcp)
    # thumb_down = thumb_tip.y > thumb_ip.y
    index_down = index_tip.y > index_pip.y
    middle_down = middle_tip.y > middle_pip.y
    pinky_down = pinky_tip.y > pinky_pip.y

    return ring_up and index_down and middle_down and pinky_down

def check_scroll_down_gesture(hand_landmarks):
    """Check if only pinky finger is up while others are down"""
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    # Check if pinky finger is up while others are down
    pinky_up = is_finger_up(pinky_tip, pinky_pip, pinky_mcp)
    # thumb_down = thumb_tip.y > thumb_ip.y
    index_down = index_tip.y > index_pip.y
    middle_down = middle_tip.y > middle_pip.y
    ring_down = ring_tip.y > ring_pip.y

    return pinky_up and index_down and middle_down and ring_down

def fingers_opened(hand_landmarks):
    tips_ids = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP,
    ]

    mids_ids = [
        mp_hands.HandLandmark.THUMB_IP,
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP,
    ]

    for tip_id, mid_id in zip(tips_ids, mids_ids):
        tip = hand_landmarks.landmark[tip_id]
        mid = hand_landmarks.landmark[mid_id]
        if tip.y >= mid.y:
            return False
    return True

def voice_control():
    global typing_enabled
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice commands...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print(f"Command received: {command}")
                if "right click" in command:
                    pyautogui.rightClick()
                elif "left click" in command:
                    pyautogui.click()
                elif "double click" in command:
                    pyautogui.doubleClick()
                elif "scroll up" in command:
                    pyautogui.scroll(500)
                elif "scroll down" in command:
                    pyautogui.scroll(-500)
                elif "start typing" in command:
                    typing_enabled = True
                    print("Typing enabled. Speak your text.")
                elif "stop typing" in command:
                    typing_enabled = False
                    print("Typing disabled.")
                elif typing_enabled:
                    pyautogui.typewrite(command)
            except sr.UnknownValueError:
                print("Sorry, could not understand the command.")
            except sr.RequestError:
                print("Could not request results; check your internet connection.")
            except sr.WaitTimeoutError:
                print("No speech detected, continuing...")

thread = threading.Thread(target=voice_control, daemon=True)
thread.start()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    frame_height, frame_width, _ = frame.shape

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger positions
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Calculate distances
            click_distance = calculate_distance(thumb_tip, index_finger_tip, frame_width, frame_height)
            zoom_distance = calculate_distance(index_finger_tip, middle_finger_tip, frame_width, frame_height)

            # Handle zoom gesture only when index and middle fingers are up
            if check_zoom_gesture(hand_landmarks):
                if prev_zoom_distance is not None:
                    zoom_diff = zoom_distance - prev_zoom_distance
                    if abs(zoom_diff) > zoom_threshold:
                        if zoom_diff > 0:  # Fingers moving apart - zoom in
                            pyautogui.hotkey('ctrl', '+')
                            print("Zoom In")
                        else:  # Fingers moving together - zoom out
                            pyautogui.hotkey('ctrl', '-')
                            print("Zoom Out")
                prev_zoom_distance = zoom_distance
            else:
                prev_zoom_distance = None  # Reset zoom tracking when gesture is not active

            # Handle clicking
            click_threshold = 30
            if click_distance < click_threshold and not left_click_active:
                left_click_active = True
                current_time = time.time()
                if current_time - last_click_time < double_click_threshold:
                    pyautogui.doubleClick()  # Trigger double-click
                    print("Double Click")
                else:
                    pyautogui.click(button='left')  # Trigger single-click
                    print("Left Click")
                last_click_time = current_time
            elif click_distance >= click_threshold:
                left_click_active = False

            if fingers_opened(hand_landmarks) and not right_click_active:
                right_click_active = True
                pyautogui.click(button='right')
                print("Right Click")
            elif not fingers_opened(hand_landmarks):
                right_click_active = False

            # Handle scroll up gesture (ring finger up)
            if check_scroll_up_gesture(hand_landmarks):
                pyautogui.scroll(500)  # Scroll up
                print("Scroll Up")

            # Handle scroll down gesture (pinky finger up)
            if check_scroll_down_gesture(hand_landmarks):
                pyautogui.scroll(-500)  # Scroll down
                print("Scroll Down")

            # Move mouse pointer
            screen_x = int(index_finger_tip.x * screen_width)
            screen_y = int(index_finger_tip.y * screen_height)
            pyautogui.moveTo(screen_x, screen_y)

            # Visual feedback
            index_x, index_y = int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)
            middle_x, middle_y = int(middle_finger_tip.x * frame_width), int(middle_finger_tip.y * frame_height)
            thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
            ring_x, ring_y = int(ring_finger_tip.x * frame_width), int(ring_finger_tip.y * frame_height)
            pinky_x, pinky_y = int(pinky_tip.x * frame_width), int(pinky_tip.y * frame_height)
            
            # Draw circles and lines for visual feedback
            cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 0), -1)  # Blue for thumb
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), -1)  # Green for index
            cv2.circle(frame, (middle_x, middle_y), 10, (0, 0, 255), -1)  # Red for middle
            cv2.circle(frame, (ring_x, ring_y), 10, (255, 255, 0), -1)  # Cyan for ring
            cv2.circle(frame, (pinky_x, pinky_y), 10, (255, 0, 255), -1)  # Purple for pinky
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 255), 2)  # Yellow for click distance
            
            # Only draw zoom distance line when gesture is active
            if check_zoom_gesture(hand_landmarks):
                cv2.line(frame, (index_x, index_y), (middle_x, middle_y), (255, 0, 255), 2)  # Purple for zoom distance

    cv2.imshow("Hand Mouse Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()