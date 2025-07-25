# Virtual Mouse: Hand Gesture and Voice Control

This project transforms your webcam into a virtual mouse controller using **hand gestures** and **voice commands**, enabling touchless computer interaction for accessibility, productivity, and learning.

## 🚀 Features

* **Hand Gesture Control:** Move the cursor, click, drag, and scroll using your hand detected via webcam.
* **Voice Command Integration:** Execute click, double-click, scroll, and exit actions using speech commands.
* **Real-time Processing:** Fast and efficient frame processing for smooth experience.
* **Cross-Platform:** Works on Windows, macOS, and Linux.

## 📂 Project Structure

* `main.py` : Main execution script to start the virtual mouse.
* `HandTrackingModule.py` : Custom hand tracking module for detecting finger positions.
* `requirements.txt` : Required Python dependencies.

## ⚙️ Installation

1️⃣ **Clone the repository:**

```bash
git clone https://github.com/vijaydasp/Virtual-Mouse-Hand-Voice.git
cd Virtual-Mouse-Hand-Voice
```

2️⃣ **Install dependencies:**

```bash
pip install -r requirements.txt
```

Dependencies include:

* `opencv-python`
* `mediapipe`
* `pyautogui`
* `speechrecognition`
* `pyaudio`

(Install `pyaudio` using `pipwin install pyaudio` on Windows if you face installation issues.)

## ▶️ Usage

Run the main script:

```bash
python main.py
```

* Show your hand in front of the webcam to control the cursor.
* Use gestures to click, drag, and scroll based on finger configurations.
* Speak commands like **"click", "double click", "scroll up", "scroll down", "exit"** to control the mouse with your voice.

## 🖐️ Gesture Control

* **Index Finger Up:** Move the cursor.
* **Index + Middle Finger Up:** Trigger clicking and dragging based on finger distance.
* **Pinch:** Can be mapped for click.
* **Specific gestures:** Customizable for advanced commands.

## 🗣️ Voice Commands

* "click" → Left Click
* "double click" → Double Click
* "right click" → Right Click
* "scroll up" → Scrolls up
* "scroll down" → Scrolls down
* "exit" → Closes the application

## 💡 Applications

✅ Accessibility for differently-abled users.
✅ Contactless control in clean environments.
✅ Learning and experimenting with computer vision and speech recognition integration.

## 🛠️ Troubleshooting

* Ensure **proper lighting** for effective hand detection.
* If the microphone doesn't capture commands:

  * Check microphone permissions.
  * Reduce background noise.
* If `pyaudio` installation fails on Windows, use:

  ```bash
  pip install pipwin
  pipwin install pyaudio
  ```

## 🤝 Contributing

Pull requests are welcome to improve gesture sets, add advanced voice commands, and enhance detection stability.

---

## 📧 Contact

**Developer:** Vijay Das

**LinkedIn:** [vijaydasp](https://www.linkedin.com/in/vijay-das-p-a42068283?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BxyyRRfIGRJ%2BYk8u1yhtC9g%3D%3D)

---

> **Empower your interaction with your computer using your hand and your voice!**
