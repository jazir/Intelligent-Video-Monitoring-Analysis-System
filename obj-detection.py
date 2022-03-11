"""
 _summary_: Detect objects from the camera feed and publish the inference meta-data to AWS IoT Core using MQTT protocol.
Pre-trained model: SSD-Mobilenet-V2
 
"""

import jetson.inference
import jetson.utils
import publish

# Load the object detection model. We are using pre-trained SSD-Mobilenet-V2 model.
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

# Create an instance of the videoSource object
camera = jetson.utils.videoSource("/dev/video0")

# Create display window
display = jetson.utils.videoOutput()

# Initialize the dictionary
dict_keys = ['frame_number', 'object', 'location', 'det_confidence']
detection_results = dict.fromkeys(dict_keys)

# Establish the connection with AWS IoT
publish.connect_client()

img_counter = 0
while display.IsStreaming():
    img = camera.Capture()  # Capture frame from camera
    img_counter += 1
    detections = net.Detect(img)  # Get the list of detections in that frame
    if (img_counter % 30) == 0:  # Send detection meta-data every 30 frames
        for detect in detections:  # Loop through all detected objects in a frame
            class_id = detect.ClassID  # Get the Class Id of the object
            # Prepase the MQTT message
            detection_results['frame_number'] = img_counter
            detection_results['object'] = net.GetClassDesc(
                class_id)  # Get the object name
            # Get the (x,y) coordinates of the object
            detection_results['location'] = detect.Center
            # Confidence value of the detection
            detection_results['det_confidence'] = detect.Confidence
            # Publish the MQTT message
            publish.publish_data(detection_results)

    display.Render(img)  # Render out this frame with detections
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(
        net.GetNetworkFPS()))  # Overlay FPS performance on the status bar

# Disconnect the client once the detection loop is exited
publish.disconnect_client()
