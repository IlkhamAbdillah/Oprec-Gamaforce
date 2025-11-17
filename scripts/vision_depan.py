#!/usr/bin/env python3
from __future__ import print_function
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):

    self.bridge = CvBridge()
    self.image_sub2 = rospy.Subscriber("/camera/color/image_raw", Image, self.callback)

  def callback(self, data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
    except CvBridgeError as e:
      print(e)
    
    (rows, cols, channels) = cv_image.shape
    center_x, center_y = cols // 2, rows // 2
    # l_bound = np.array([0, 0, 102])
    # u_bound = np.array([0, 0, 255])
    l_bound = np.array([0, 112, 255])
    u_bound = np.array([0, 112, 255])
    # l_bound = np.array([0,0,102])
    # u_bound = np.array([0,0,255])
    masked_img = cv2.inRange(cv_image, l_bound, u_bound)
    
    contours, _ = cv2.findContours(masked_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on minimum size
    min_contour_size = 100  # Adjust this value based on your requirements
    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_size]
    
    # Calculate moments for the largest contour
    '''if filtered_contours:
      largest_contour = max(filtered_contours, key=cv2.contourArea)
      moments = cv2.moments(largest_contour)

    # Avoid division by zero
    if moments['m00'] != 0:
            # Calculate the centroid (center) of the contour
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00']) + 22

            # Print or use the centroid coordinates as needed
            print("Contour center:", cx, cy)

            # Draw a small circle at the centroid
            cv2.circle(cv_image, (cx, cy), 6, (255, 255, 255), -1)

    '''
    cv2.drawContours(cv_image, filtered_contours, 0, (0, 255, 0), 2)

    # Define the length of the crosshair lines
    crosshair_length = 20

    # Draw horizontal line (crosshair)
    cv2.line(cv_image, (center_x - crosshair_length, center_y), (center_x + crosshair_length, center_y), (255, 255, 255), 2)

    # Draw vertical line (crosshair)
    cv2.line(cv_image, (center_x, center_y - crosshair_length), (center_x, center_y + crosshair_length), (255, 255, 255), 2)
    
    cv2.imshow("lihat bawah", cv_image)
    cv2.waitKey(3)

def main(args):
  ic = image_converter()
  rospy.init_node('image_bawahe', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main(sys.argv)
