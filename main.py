import numpy as np
from run_animation import *
import time

###Options - Do not need to modify
##################################

#Vectors to Use
verticality_vec = ('WaistRBack', 'BackRight')
arm_left = ('RShoulderBack', 'RWristOut')
arm_right = ('LShoulderBack', 'LWristOut')
leg_left = ('WaistRBack', 'RAnkleOut')
leg_right = ('WaistLBack', 'LAnkleOut')
random_periodic = ('Random', 'Periodic')

#Paths to plot for Human skeleton
paths = [('BackTop','HeadTop'),('BackLeft','BackRight'),\
		('WaistLBack','WaistRBack'),\
		('RHandOut','RWristOut'), ('RWristOut','RElbowOut'), \
		('RElbowOut', 'RShoulderBack'), ('RShoulderBack', 'BackTop'), \
		('BackTop','BackRight'), ('BackRight','WaistRBack'), \
		('WaistRBack', 'RKneeOut'), ('RKneeOut', 'RAnkleOut'), \
		('RAnkleOut', 'RToeOut'), \
		('LHandOut','LWristOut'), ('LWristOut','LElbowOut'), \
		('LElbowOut', 'LShoulderBack'), ('LShoulderBack', 'BackTop'), \
		('BackTop','BackLeft'), ('BackLeft','WaistLBack'), \
		('WaistLBack', 'LKneeOut'), ('LKneeOut', 'LAnkleOut'), \
		('LAnkleOut', 'LToeOut')]

#Variables to Modify#############################################################
#################################################################################
#Positions
left_pos = np.array([[0,2,0]])
mid_pos = np.array([[0,0,0]])
right_pos = np.array([[0,-2,0]])

#Video Options
video_filename = 'test01.mp4'
save_type = 'animate' #animate or video
animation_speed = 0.03
img_flag = False
video_title = ''

#Mover Options
human_mover = {'type': 'human', 'pos': mid_pos, 'paths': paths, \
			'section': range(15000,17000), 'filename': 'mocapdata01.npz'}
broombot_vert_right = {'type': 'broombot', 'pos': right_pos, 'vector': verticality_vec, \
			'section': range(15000,17000), 'filename': 'mocapdata01.npz', \
			'radius': 0.25, 'height': 0.5, 'n': 10}
rollbot_mover = {'type': 'rollbot', 'pos': mid_pos, 'vector': random_periodic, \
			'section': range(0,1), 'filename': 'mocapdata01.npz',\
			'radius': 0.25, 'height': 0.2, 'stretch': 1.5}
mover_opt = [rollbot_mover]

#Do not need to modify variables below this line most of the time################
#################################################################################

#Video Options
video_fps = 120
ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg'
elevation = 23
azimuth = -180
plane_start = -5
plane_end = 5
height_max = 5
color_key = ['green', 'red']

#Create inputs to function	
video_opt = {'video_filename': video_filename, 'save_type': save_type, \
			'video_title': video_title, 'video_fps': video_fps, \
			'ffmpeg_path': ffmpeg_path, 'elevation': elevation, \
			'azimuth': azimuth, 'plane_start': plane_start, \
			'plane_end': plane_end, 'height_max': height_max, \
			'color_key': color_key, 'img_flag': img_flag, \
			'animation_speed': animation_speed}

run_animation(video_opt, mover_opt)