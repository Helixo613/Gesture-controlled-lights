# Gesture-Controlled LED Display  

This project uses **MediaPipe** and **OpenCV** for real-time hand tracking to control **LEDs on an Arduino board**. The system detects the distance between the **thumb and index finger** and dynamically adjusts the number of LEDs that light up. A maximum of **five LEDs** illuminate when the fingers are fully separated.

## 📜 Table of Contents  
- [Overview](#overview)  
- [Features](#features)  
- [Components](#components)  
- [Hardware Setup](#hardware-setup)  
- [Software Setup](#software-setup)  
- [Usage](#usage)  
- [Future Improvements](#future-improvements)  

## 🚀 Overview  
The project tracks **hand gestures** using a webcam and controls LEDs based on the distance between the **thumb and index finger**. The further apart the fingers are, the more LEDs light up, with a maximum of **five LEDs** turning on.

## ✨ Features  
✔ **Real-time Hand Tracking** – Uses **MediaPipe** and **OpenCV** for accurate gesture detection.  
✔ **Distance-Based LED Control** – Adjusts the number of lit LEDs based on finger distance.  
✔ **Arduino Integration** – Sends commands to an **Arduino board** to control LEDs.  
✔ **Dynamic Adjustments** – LEDs light up in real-time as the user moves their fingers.  

## 🔧 Components  

### **Hardware**  
- **Arduino board** (with at least 5 digital pins)  
- **5 LEDs**  
- **220Ω resistors** (one per LED)  
- **Breadboard**  
- **Jumper wires**  
- **Webcam**  

### **Software**  
- **Python 3.x**  
- **MediaPipe**  
- **OpenCV**  
- **NumPy**  
- **PySerial**  
- **Arduino IDE**  

## 🛠️ Hardware Setup  
1. Connect **5 LEDs** to the Arduino using the following pin configuration:  
   - **LED 1 → Pin 2**  
   - **LED 2 → Pin 4**  
   - **LED 3 → Pin 8**  
   - **LED 4 → Pin 10**  
   - **LED 5 → Pin 12**  
2. Attach a **220Ω resistor** to each LED.  
3. Connect all LED grounds to the **GND** pin on the Arduino.  
4. Use a **USB cable** to connect the Arduino to your computer.  

## 🖥️ Software Setup  
### Step 1: Install Dependencies  
Run the following command to install the required Python libraries:  

```bash
pip install mediapipe opencv-python numpy pyserial
