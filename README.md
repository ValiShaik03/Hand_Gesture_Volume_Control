<h1>🖐 Gesture-Based Volume Control Using Python & OpenCV</h1>
Control your system volume using hand gestures captured via webcam! This project uses Python, OpenCV, and MediaPipe to detect finger distance and adjust system audio dynamically.

🛠 Tech Stack<br>

*Python<br>
*OpenCV<br>
*MediaPipe<br>
*Pycaw (for system audio control)<br>
*NumPy<br>
*Math (for calculating distances)<br>

🚀 Features<br>

*Real-time webcam-based hand gesture detection

*Volume control by adjusting distance between thumb and index finger

*Displays current volume level and FPS on screen

*Visual feedback with dynamic bar and volume percentage<br>

📂 Installation & Setup<br>
1.Clone the repository
```bash
git clone https://github.com/your-username/gesture-volume-control.git
cd gesture-volume-control
```
2.Install Dependencies
```bash
pip install -r requirements.txt
```
3.Run the project
```bash
python main.py
```
✋ How It Works<br>

*Uses MediaPipe to detect hand landmarks<br>
*Maps the distance range to system volume range<br>
*Uses Pycaw to control system volume in real time<br>
*Displays volume level and FPS on screen with OpenCV<br>

📸 Project Demo <br>

https://www.loom.com/share/b1be6fa3b37a4e8a94c7a447ada47330?sid=9b6cd25e-8b0a-4d12-95a4-11a256cd055d

🙌 Acknowledgments<br>
*MediaPipe by Google<br>
*Pycaw for volume control<br>

📃 License<br>
This project is licensed under the MIT License.
