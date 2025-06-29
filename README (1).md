# ✋ Gesture-Controlled Virtual Calculator

A hand gesture-controlled calculator using **OpenCV**, **MediaPipe**, and **Python**.  
Control the calculator by showing your hand gestures — no mouse or keyboard needed!

---

## 🎥 Demo

> Hover your index finger over the buttons for **1 second** to click using gesture.

![Demo Screenshot](screenshot.png)

---

## 🚀 Features

- 🖐️ Recognizes **5 fingers** open to activate control
- ☝️ **Index finger** acts as pointer
- 🕐 **1-second hover** triggers button press
- ➕ Basic math operations: `+`, `-`, `*`, `/`
- 🔄 `C` to clear, `=` to evaluate
- 🎨 Modern UI with:
  - Button box
  - Color-coded buttons
  - Transparent background effect

---

## 📦 Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

Manual installation:

```bash
pip install opencv-python mediapipe numpy
```

---

## 🧠 How It Works

- Uses **MediaPipe** to detect hand landmarks
- Tracks **index finger tip** (Landmark #8)
- Counts **total fingers up** to allow input
- Detects if finger hovers on button for 1 second → registers click

---

## 💻 How to Run

```bash
python gesture_calculator_fast_theme.py
```

Press `q` to exit the app.

---

## 📁 Project Structure

```
GestureCalculator/
│
├── gesture_calculator_fast_theme.py  # Main code
├── requirements.txt                  # Dependencies
├── screenshot.png                    # Optional: demo image
└── README.md                         # This file
```

---

## 🤖 Future Ideas

- 📱 Android version using MediaPipe Hands on mobile
- 🎵 Add sound feedback on button press
- 💬 Voice support: read the result aloud

---

## 🙌 Created By

**Harsha** — built with ❤️ using Python and OpenCV  
Contributions welcome!