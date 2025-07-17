import mediapipe as mp
import cv2
import numpy as np
import random
import time

# Initialize MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Game variables
score = 0
x_enemy = random.randint(50, 600)
y_enemy = random.randint(50, 400)
ENEMY_RADIUS = 25  # Radius of the enemy circle
FINGER_TIP_RADIUS = 25 # Visual radius for the index finger tip

# Timer variables
GAME_DURATION = 0 # Will be set by user input
start_time = None
game_active = True # Flag to control game state

# --- User Input for Game Duration ---
def get_game_duration():
    while True:
        try:
            print("Select Game Duration:")
            print("1. 30 seconds")
            print("2. 60 seconds")
            print("3. 120 seconds")
            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == '1':
                return 30
            elif choice == '2':
                return 60
            elif choice == '3':
                return 120
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")

GAME_DURATION = get_game_duration()
print(f"Game will run for {GAME_DURATION} seconds. Get ready!")
time.sleep(2) # Give user a moment to see confirmation before webcam opens

# Function to draw the enemy
def draw_enemy(image):
    cv2.circle(image, (x_enemy, y_enemy), ENEMY_RADIUS, (0, 200, 0), 5)

video = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not video.isOpened():
    print("Error: Could not open video stream.")
    exit()

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    # Set the start time when the game loop effectively begins
    start_time = time.time()

    while video.isOpened() and game_active:
        ret, frame = video.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Flip the frame horizontally for a mirrored view
        image = cv2.flip(frame, 1)
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Get image dimensions
        imageHeight, imageWidth, _ = image.shape

        # Process the image with MediaPipe Hands
        results = hands.process(image_rgb)

        # Convert the RGB image back to BGR for OpenCV display
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        # --- Timer Logic ---
        elapsed_time = time.time() - start_time
        remaining_time = max(0, GAME_DURATION - int(elapsed_time)) # Calculate remaining time as integer

        if remaining_time == 0:
            game_active = False # Set game_active to False to break the loop

        # Display the timer and score
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 0, 255) # Magenta color

        cv2.putText(image, "Score:", (480, 30), font, 1, color, 2, cv2.LINE_AA)
        cv2.putText(image, str(score), (590, 30), font, 1, color, 2, cv2.LINE_AA)

        cv2.putText(image, f"Time: {remaining_time}s", (10, 30), font, 1, (0, 255, 255), 2, cv2.LINE_AA) # Cyan for time

        # Draw the enemy only if the game is active
        if game_active:
            draw_enemy(image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                              mp_drawing.DrawingSpec(color=(250, 250, 250), thickness=2, circle_radius=2))

                    # Get the coordinates of the index finger tip
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    index_tip_x = int(index_finger_tip.x * imageWidth)
                    index_tip_y = int(index_finger_tip.y * imageHeight)

                    # Draw a circle at the index finger tip for better visualization
                    cv2.circle(image, (index_tip_x, index_tip_y), FINGER_TIP_RADIUS, (0, 255, 255), 5) # Cyan circle

                    # --- Collision Detection ---
                    # Calculate the distance between the index finger tip and the enemy center
                    distance = np.sqrt((index_tip_x - x_enemy)**2 + (index_tip_y - y_enemy)**2)

                    # If the distance is less than the sum of their radii, a collision has occurred
                    if distance < (ENEMY_RADIUS + FINGER_TIP_RADIUS):
                        score += 1
                        # Reposition the enemy
                        x_enemy = random.randint(50, imageWidth - 50)
                        y_enemy = random.randint(50, imageHeight - 50)
                        print(f"Hit! Score: {score}")
        else:
            # Game Over screen
            game_over_text = "GAME OVER!"
            final_score_text = f"Final Score: {score}"

            # Get text size to center it
            (text_width, text_height), _ = cv2.getTextSize(game_over_text, font, 2, 3)
            (score_width, score_height), _ = cv2.getTextSize(final_score_text, font, 1.5, 2)

            # Calculate center positions
            center_x_go = (imageWidth - text_width) // 2
            center_y_go = (imageHeight + text_height) // 2 - 50 # Slightly above center

            center_x_score = (imageWidth - score_width) // 2
            center_y_score = center_y_go + text_height + 30 # Below "GAME OVER!"

            cv2.putText(image, game_over_text, (center_x_go, center_y_go), font, 2, (0, 0, 255), 3, cv2.LINE_AA) # Red
            cv2.putText(image, final_score_text, (center_x_score, center_y_score), font, 1.5, (255, 255, 0), 2, cv2.LINE_AA) # Yellow

        cv2.imshow('TapNPop Game', image) # Changed window title

        # --- Check for 'q' or 'Esc' key press to quit ---
        key_pressed = cv2.waitKey(10) & 0xFF
        if key_pressed == ord('q') or key_pressed == 27: # 27 is the ASCII for Esc key
            print("Game exited by user.")
            print(f"Final Score: {score}")
            break

video.release()
cv2.destroyAllWindows()