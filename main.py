import keyboard
import numpy as np
import time

keys = ['left arrow', 'right arrow', 'up arrow', 'down arrow']

# keyboard.press_and_release('left arrow')

# Python program to implement
# Webcam Motion Detector

# importing OpenCV, time and Pandas library
import cv2, time, pandas
# importing datetime class from datetime library
from datetime import datetime

# Assigning our static_back to None
static_back = None

# List when any moving object appear
motion_list = [ None, None ]

# Time of movement
# time = []

# Initializing DataFrame, one column is start
# time and other column is end time
df = pandas.DataFrame(columns = ["Start", "End"])

# Capturing video
video = cv2.VideoCapture(0)

w = 480
h = 640
centers = []

# Radius of circle
radius = 50

# Blue color in BGR
color = (0, 255, 0)

# Line thickness of 2 px
thickness = 2
masks = []
actions = ['left arrow', 'up arrow', 'right arrow']
tot_mask = []

for i in range(len(actions)):
	action = actions[i]
	center_coordinates = (0,0)
	if i == 0:
		center_coordinates = (radius+50, w//2+1)
	elif i == 1:
		center_coordinates = (h//2 + 1, radius)
	elif i == 2:
		center_coordinates = (h-radius-50, w//2+1)
	else:
		exit(1)
	centers.append(center_coordinates)
	mask = np.zeros((w, h), np.uint8)
	m = np.zeros((w,h,3), np.uint8)
	for i in range(w):
		for j in range(h):
			if (j - center_coordinates[0]) * (j - center_coordinates[0]) + (i - center_coordinates[1]) * (
					i - center_coordinates[1]) <= (radius * radius):
				mask[i][j] = 255
				m[i][j][0] = 255
				m[i][j][1] = 255
				m[i][j][2] = 255
	masks.append(mask)
	tot_mask.append(m)

union_mask = np.zeros((w,h,3), np.uint8)
for mask in tot_mask:
	union_mask = np.bitwise_or(union_mask, mask)

moved = False

# Infinite while loop to treat stack of image as video
while True:
	# Reading frame(image) from video
	check, frame = video.read()
	# print(frame.shape)
	frame = cv2.flip(frame, 1)
	# print(frame.shape)
	motion = 0

	# Converting color image to gray_scale image
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Converting gray scale image to GaussianBlur
	# so that change can be find easily
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	# print(gray.shape)

	# In first iteration we assign the value
	# of static_back to our first frame
	if static_back is None:
		static_back = gray
		continue

	# Difference between static background
	# and current frame(which is GaussianBlur)
	diff_frame = cv2.absdiff(static_back, gray)

	# If change in between static background and
	# current frame is greater than 30 it will show white color(255)
	thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
	thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

	# h, w = thresh_frame.shape
	# print(h, w, mask.shape)
	# frame = np.bitwise_and(frame, mask)

	# Displaying image in gray_scale
	# cv2.imshow("Gray Frame", gray)

	# Displaying the difference in currentframe to
	# the staticframe(very first_frame)
	# cv2.imshow("Difference Frame", diff_frame)

	# Displaying the black and white image in which if
	# intensity difference greater than 30 it will appear white
	for center_coordinates in centers:
		frame = cv2.circle(frame, center_coordinates, radius, color, thickness)
		thresh_frame = cv2.circle(thresh_frame, center_coordinates, radius, color, thickness)
	# cv2.imshow("Threshold Frame", thresh_frame)

	# frame = np.bitwise_and(frame, union_mask)

	# print(frame.shape)
	cv2.imshow("Color Frame", frame)

	temp = False
	for i in range(len(actions)):
		action = actions[i]
		mask = masks[i]
		res = cv2.bitwise_and(thresh_frame, mask)
		motion = np.count_nonzero(res)
		# if motion > 0:
			# print(motion)
		if motion > 1000:
			temp = action
			if moved != action:
				print('moving', action)
				keyboard.press_and_release(action)
				# time.sleep(5)
	moved = temp

	# if moved == False:
	# 	static_back = gray

	# print('moved', moved)

	key = cv2.waitKey(1)
	# if q entered whole process will stop
	if key == ord('q'):
		break


video.release()

# Destroying all the windows
cv2.destroyAllWindows()
