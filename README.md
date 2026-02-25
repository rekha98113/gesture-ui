Gesture Controlled UI
🚀 Overview

Gesture Controlled UI is a computer vision–based interface that allows users to control system applications using hand gestures instead of traditional input devices like a mouse or keyboard.

The system uses real-time camera input to detect hand landmarks, interpret gestures, and map them to system-level actions such as cursor movement, clicking, volume control, and scrolling.

This project explores touchless interaction using AI-powered vision systems, improving accessibility and enabling futuristic human-computer interaction.

🎯 Problem Statement

Traditional input devices limit interaction flexibility and accessibility. This project aims to create a hands-free interaction system using real-time gesture recognition to:

Improve accessibility for users with mobility constraints

Enable touchless interaction in hygienic environments

Demonstrate real-time computer vision applications

🧠 How It Works

Captures live video feed from the system camera

Detects hand landmarks using computer vision

Identifies gesture patterns based on finger positions

Maps gestures to predefined UI actions

Executes system commands in real-time

The core logic involves tracking fingertip coordinates and calculating distances/angles to classify gestures.

🛠️ Tech Stack

Python

OpenCV

MediaPipe (Hand Landmark Detection)

PyAutoGUI (System Control Automation)

✨ Features

Real-time hand tracking

Cursor movement using index finger

Left and right click detection

Volume control using pinch gesture

Scroll functionality

Low-latency gesture recognition
