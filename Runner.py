"""
Hand Gesture to Serial Communication

This script captures video from a camera, detects hand gestures, calculates the
distance between fingertips, scales the distance, and sends the scaled value
to a serial port.

Dependencies:
    - OpenCV (cv2)
    - PySerial (serial)
    - A custom 'Hands.py' module with Hand class and map_distance_to_scale function.

Usage:
    1. Ensure your camera is connected.
    2. Run the script.
    3. Select the correct COM port from the list displayed.
    4. The script will continuously send scaled distance data to the serial port.

Author: Arnav Bansal/Helixo613
Date: 15-06-2024
"""

from Hands import Hand, map_distance_to_scale  # Import custom hand detection and scaling functions
import cv2  # Import OpenCV for image processing
import serial  # Import PySerial for serial communication
import serial.tools.list_ports as sp  # Import tools to list serial ports
import time  # Import time for delays

def runner():
    """
    Captures video, detects hand gestures, calculates distance, scales it,
    and sends the data to the serial port.
    """
    # --- Serial Port Selection ---
    ports = sp.comports()  # Get a list of available serial ports
    serial_ = serial.Serial()  # Initialize a serial object
    available_ports = [str(port) for port in ports]  # Convert port descriptions to strings
    print("Available COM Ports:")
    for port in available_ports:
        print(f"- {port}")  # Print each available port

    com = input("Select COM port: ")  # Prompt user to select a COM port
    selected_port = None  # Initialize selected port variable
    for port in available_ports:
        if port.startswith(f"COM{com}"):  # Check if port matches user input
            selected_port = f"COM{com}"  # Set the selected port
            break

    if not selected_port:  # Check if a valid port was selected
        print(f"COM{com} not found. Exiting.")
        return  # Exit the function if port not found

    # --- Serial Port Configuration and Opening ---
    serial_.baudrate = 9600  # Set baud rate
    print(f"Using port: {selected_port}")  # Print selected port
    serial_.port = selected_port  # Set the serial port
    try:
        serial_.open()  # Open the serial port
    except serial.SerialException as e:  # Handle serial port opening errors
        print(f"Error opening serial port: {e}")
        return  # Exit function if error occurs

    # --- Camera and Hand Detection Initialization ---
    camera = cv2.VideoCapture(0)  # Initialize camera (0 for default camera)
    detector = Hand(trac_conf=0.9, det_conf=0.9)  # Initialize hand detection object
    last_sent_data = ""  # Initialize variable to store last sent data

    # --- Main Loop: Capture, Process, and Send Data ---
    try:
        while True:
            ret, frame = camera.read()  # Read a frame from the camera
            if not ret:  # Check if frame was read successfully
                print("Error reading frame. Exiting.")
                break  # Exit loop if frame error

            detector.get_hand(frame)  # Detect hands in the frame
            detector.draw_line(frame, draw=True)  # Draw line between fingertips
            scaled_distance = str(map_distance_to_scale(detector.line_dist)) + "\n"  # Scale distance and add newline

            if scaled_distance != last_sent_data:  # Check if data has changed
                try:
                    serial_.write(scaled_distance.encode('utf-8'))  # Send data to serial port
                    print(f"Sent: {scaled_distance.strip()}")  # Print sent data
                    last_sent_data = scaled_distance  # Update last sent data
                except serial.SerialException as e:  # Handle serial port writing errors
                    print(f"Serial port error: {e}")
                    break  # Exit loop if error occurs

            cv2.imshow("Hand Gesture Control", frame)  # Display the frame
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Check for 'q' key press to exit
                break  # Exit loop if 'q' is pressed

            time.sleep(1 / 24)  # Control frame rate (approximately 24 FPS)

    except KeyboardInterrupt:  # Handle keyboard interrupt (Ctrl+C)
        print("\nScript interrupted by user.")
    finally:  # Cleanup resources
        camera.release()  # Release camera resources
        cv2.destroyAllWindows()  # Close OpenCV windows
        if serial_.is_open:  # Close serial port if it's open
            serial_.close()
            print("Serial port closed.")

if __name__ == "__main__":
    runner()  # Call the runner function when script is executed