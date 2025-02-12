#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()

    def listener_callback(self, data):
        # Convert ROS Image message to OpenCV image
        current_frame = self.bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
        
        # Convert BGR to HSV
        hsv_image = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)

        # Define range of green color in HSV
        lower_green = np.array([40, 40, 40])   # Lower bound of green color
        upper_green= np.array([80, 255, 255])  # Upper bound of green color
        
        # Define range of blue color in HSV
        lower_green = np.array([40, 40, 40])   # Lower bound of blue color
        upper_green= np.array([80, 255, 255])  # Upper bound of blue color
        
        # Define range of red color in HSV
        lower_green = np.array([40, 40, 40])   # Lower bound of red color
        upper_green= np.array([80, 255, 255])  # Upper bound of red color

        # Create a binary mask
        blue_mask = cv2.inRange(hsv_image, lower_green, upper_green)

        # Apply the mask to the original image
        blue_segmented_image = cv2.bitwise_and(current_frame, current_frame, mask=blue_mask)

        
        
        # Display the segmented image
        cv2.imshow("Blue Segmented Image", blue_segmented_image)
        cv2.waitKey(1)

    
def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

       
    
