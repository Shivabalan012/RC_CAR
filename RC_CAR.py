import serial                                                                   
import time                                                                     
import mraa                                                                     
                                                                                
# Initialize Bluetooth                                                          
try:                                                                            
    bluetooth = serial.Serial("/dev/ttyS3", baudrate=38400, timeout=1)          
    print("Connected to /dev/ttyS3 at 38400 baud")                              
except serial.SerialException:                                                  
    print("Failed to connect to Bluetooth")                                     
    exit()                                                                      
                                                                                
# Define motor control pins                                                     
MOTOR1_FWD = mraa.Gpio(23)  # Motor 1 Forward                                   
MOTOR1_BWD = mraa.Gpio(24)  # Motor 1 Backward                                  
MOTOR2_FWD = mraa.Gpio(14)                                                      
MOTOR2_BWD = mraa.Gpio(15)                                                      
                                                                                
# Define Ultrasonic Sensor Pins                                                 
TRIG_PIN = 12                                                                   
ECHO_PIN = 13                                                                   
                                                                                
# Initialize GPIO as output for motors                                          
for pin in [MOTOR1_FWD, MOTOR1_BWD, MOTOR2_FWD, MOTOR2_BWD]:                    
    pin.dir(mraa.DIR_OUT)                                                       
    pin.write(0)  # Set motors off initially                                    
                                                                                
# Initialize GPIO for ultrasonic sensor                                         
trigPin = mraa.Gpio(TRIG_PIN)                                                   
echoPin = mraa.Gpio(ECHO_PIN)                                                   
trigPin.dir(mraa.DIR_OUT)                                                       
echoPin.dir(mraa.DIR_IN)                                                        
                                                                                
def measure_distance():                                                         
    # Send Trigger Pulse                                                        
    trigPin.write(0)                                                            
    time.sleep(0.00001)  # 10µs delay                                           
    trigPin.write(1)                                                            
    time.sleep(0.00001)  # 10µs pulse                                           
    trigPin.write(0)                                                            
                                                                                
    # Wait for Echo to go HIGH (start time)                                     
    start_time = time.time()                                                    
    timeout = start_time + 0.02  # 20ms timeout                                 
    while echoPin.read() == 0:                                                  
        start_time = time.time()                                                
        if start_time > timeout:                                                
            return None  # No valid measurement                                 
                                                                                
    # Wait for Echo to go LOW (stop time)                                       
    stop_time = time.time()                                                     
    timeout = stop_time + 0.02  # 20ms timeout                                  
    while echoPin.read() == 1:                                                  
        stop_time = time.time()                                                 
        if stop_time > timeout:                                                 
            return None  # No valid measurement                                 
                                                                                
    # Calculate time difference                                                 
    elapsed_time = stop_time - start_time                                       
    distance = (elapsed_time * 34300) / 2  # Speed of sound in cm/s             
                                                                                
    return distance                                                             
                                                                                
def stop_motors():                                                              
    print("Executing: Stopping Motors")                                         
    MOTOR1_FWD.write(0)                                                         
    MOTOR2_FWD.write(0)                                                         
    MOTOR1_BWD.write(0)                                                         
    MOTOR2_BWD.write(0)                                                         
                                                                                
def send_data(data):                                                            
    """Send data to HC-05"""                                                    
    bluetooth.write((data + "\n").encode())  # Ensure newline for proper reading
    print("Sent: " + data)                                                      
                                                                                
def receive_data():                                                             
    """Receive data from HC-05"""                                               
    try:                                                                        
        if bluetooth.in_waiting > 0:                                            
            data = bluetooth.readline().decode().strip()                        
            if data:                                                            
                print("Received Command: {}".format(data))  # Log received commd
            return data                                                         
    except Exception as e:                                                      
        print("Error receiving data: ", str(e))                                 
    return None                                                                 
                                                                                
try:                                                                            
    print("Bluetooth HC-05 Module Connected! Waiting for commands...")          
                                                                                
    while True:                                                                 
        distance = measure_distance()                                           
        if distance is not None and distance < 10:                              
            print("Object detected within 10cm! Stopping motors.")              
            stop_motors()                                                       
            send_data("Obstacle detected, motors stopped")                      
            continue  # Skip command processing when an obstacle is detected    
                                                                                
        received_text = receive_data()                                          
        if received_text:                                                       
            command = received_text.lower()                                     
            print("Processing Command: {}".format(command))  # Log command befon
                                                                                
            if command == "forward":                                            
                MOTOR1_FWD.write(1)                                             
                MOTOR2_FWD.write(1)                                             
                MOTOR1_BWD.write(0)                                             
                MOTOR2_BWD.write(0)                                             
            elif command == "backward":                                         
                MOTOR1_FWD.write(0)                                             
                MOTOR2_FWD.write(0)                                             
                MOTOR1_BWD.write(1)                                             
                MOTOR2_BWD.write(1)                                             
            elif command == "left":                                             
                MOTOR1_FWD.write(0)                                             
                MOTOR2_FWD.write(1)                                             
                MOTOR1_BWD.write(1)                                             
                MOTOR2_BWD.write(0)                                             
            elif command == "right":                                            
                MOTOR1_FWD.write(1)                                             
                MOTOR2_FWD.write(0)                                             
                MOTOR1_BWD.write(0)                                             
                MOTOR2_BWD.write(1)                                             
            elif command == "stop":                                             
                stop_motors()                                                   
            else:                                                               
                print("Unknown command received")                               
                                                                                
            send_data("ACK: {}".format(command))  # Acknowledge command         
        time.sleep(0.1)                                                         
                                                                                
except KeyboardInterrupt:                                                       
    print("\nStopping Motors and Exiting...")                                   
    stop_motors()                                                               
    bluetooth.close()