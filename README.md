# RC_CAR
This project implements a Bluetooth-controlled robot with ultrasonic obstacle detection using the MRAA library for GPIO control. The robot receives movement commands via HC-05 Bluetooth module and stops automatically if an obstacle is detected within 10 cm.
**🛠 Features**
📡 Bluetooth Communication: Receives commands (forward, backward, left, right, stop) from a paired device.

🔄 Motor Control: Uses GPIO pins to control two motors.

🔊 Ultrasonic Sensor: Measures distance and stops the motors when an obstacle is detected.

📩 Real-time Feedback: Sends acknowledgment and obstacle alerts back to the controller.
**📜 Dependencies******
Python

serial (for Bluetooth communication)

mraa (for GPIO handling)
🏗 Hardware Requirements
RuggedBoard A5D2X / Any MRAA-supported board

HC-05 Bluetooth Module

Motor Driver (L298N or equivalent)

Two DC Motors

Ultrasonic Sensor (HC-SR04)

Power Supply (5V/3.3V)
