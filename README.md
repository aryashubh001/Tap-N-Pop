# Tap-N-Pop
TapNPop is an interactive, webcam-based game that challenges your hand-eye coordination! Using MediaPipe for advanced hand tracking, you control an on-screen pointer with your index finger. The objective is to "pop" the green target circle by touching it with your index finger tip to score points. The game runs for a fixed 30-second duration, after which your final score is displayed.
✨ Features
Real-time Hand Tracking: Utilizes Google's MediaPipe framework to detect and track your hand landmarks in real-time.

Index Finger Pointer: Your index finger tip is highlighted with a distinct circle, acting as your in-game pointer.

Dynamic Target: A green circle (the "enemy") appears randomly on the screen and changes position every time you successfully "pop" it.

Score Counter: Keep track of how many targets you've hit.

30-Second Time Limit: The game automatically ends after 30 seconds, challenging you to score as much as possible within the timeframe.

Game Over Screen: Displays your final score clearly once the time runs out.

Intuitive Controls: Simple and natural interaction using hand gestures.

Easy Exit: Press Q or Esc at any time to quit the game.
🚀 Technologies Used
Python: The core programming language.

MediaPipe (Google): For robust and real-time hand detection and landmark extraction.

OpenCV (Open Source Computer Vision Library): For webcam access, image processing, drawing graphics, and displaying the game window.

NumPy: Essential for numerical operations, especially in collision detection.
