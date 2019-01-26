import numpy as np
from run_animation import *
import time

##Single Video Generation

#Vectors
verticality_vec = ('WaistRBack', 'BackRight')
arm_left = ('RShoulderBack', 'RWristOut')
arm_right = ('LShoulderBack', 'LWristOut')
leg_left = ('WaistRBack', 'RAnkleOut')
leg_right = ('WaistLBack', 'LAnkleOut')
random_periodic = ('Random', 'Periodic')

#Positions
left_pos = np.array([[0,2,0]])
mid_pos = np.array([[0,0,0]])
right_pos = np.array([[0,-2,0]])

#File Options
start_ind = 0
end_ind = 1
filename = 'mocapdata01.npz'
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
file_opt = {'section': range(start_ind,end_ind), \
		'filename': filename, 'paths': paths}

#Video Options
video_filename = 'test.mp4'
video_flag = True
video_title = ''
video_fps = 120
ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg'
elevation = 15
azimuth = -180
plane_start = -5
plane_end = 5
height_max = 5
color_key = ['green', 'red']		
video_opt = {'video_filename': video_filename, 'video_flag': video_flag, \
			'video_title': video_title, 'video_fps': video_fps, \
			'ffmpeg_path': ffmpeg_path, 'elevation': elevation, \
			'azimuth': azimuth, 'plane_start': plane_start, \
			'plane_end': plane_end, 'height_max': height_max, \
			'color_key': color_key}

#Mover Options
mover1 = {'type': 'human', 'pos': mid_pos}
mover_opt = [mover1]

run_animation(file_opt, video_opt, mover_opt)
end = time.clock()

########################################################################################
##Multiple Video Generation

# code1 = ['A', 'V', 'L']
# start_ind_vec = [0, 3000, 23000]
# end_ind_vec = [3000, 7000, 26000]
# code2 = ['V', 'AL', 'AR', 'LL', 'LR', 'RP']
# vectors = [verticality_vec, arm_left, arm_right, leg_left, leg_right, random_periodic]

# counter = 1
# for ind1 in range(3):
# 	for ind2 in range(6):
# 		for ind3 in range(6):
# 			start = time.clock()
# 			if counter > 54:
# 				#File Options
# 				start_ind = start_ind_vec[ind1]
# 				end_ind = end_ind_vec[ind1]
# 				filename = 'mocapdata01.npz'
# 				paths = [('BackTop','HeadTop'),('BackLeft','BackRight'),\
# 						('WaistLBack','WaistRBack'),\
# 						('RHandOut','RWristOut'), ('RWristOut','RElbowOut'), \
# 						('RElbowOut', 'RShoulderBack'), ('RShoulderBack', 'BackTop'), \
# 						('BackTop','BackRight'), ('BackRight','WaistRBack'), \
# 						('WaistRBack', 'RKneeOut'), ('RKneeOut', 'RAnkleOut'), \
# 						('RAnkleOut', 'RToeOut'), \
# 						('LHandOut','LWristOut'), ('LWristOut','LElbowOut'), \
# 						('LElbowOut', 'LShoulderBack'), ('LShoulderBack', 'BackTop'), \
# 						('BackTop','BackLeft'), ('BackLeft','WaistLBack'), \
# 						('WaistLBack', 'LKneeOut'), ('LKneeOut', 'LAnkleOut'), \
# 						('LAnkleOut', 'LToeOut')]
# 				file_opt = {'section': range(start_ind,end_ind), \
# 						'filename': filename, 'paths': paths}

# 				#Video Options
# 				video_filename = code1[ind1] + '_' + code2[ind2] + '_' + code2[ind3] + '.mp4'
# 				video_flag = True
# 				video_title = ''
# 				video_fps = 120
# 				ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg'
# 				elevation = 15
# 				azimuth = -180
# 				plane_start = -5
# 				plane_end = 5
# 				height_max = 5
# 				color_key = ['green', 'red']		
# 				video_opt = {'video_filename': video_filename, 'video_flag': video_flag, \
# 							'video_title': video_title, 'video_fps': video_fps, \
# 							'ffmpeg_path': ffmpeg_path, 'elevation': elevation, \
# 							'azimuth': azimuth, 'plane_start': plane_start, \
# 							'plane_end': plane_end, 'height_max': height_max, \
# 							'color_key': color_key}

# 				#Mover Options
# 				mover1 = {'type': 'human', 'pos': mid_pos}
# 				mover2 = {'type': 'broombot', 'pos': left_pos, 'vector': vectors[ind2], \
# 					'radius': 0.25, 'height': 0.5, 'n': 10}
# 				mover3 = {'type': 'broombot', 'pos': right_pos, 'vector': vectors[ind3], \
# 					'radius': 0.25, 'height': 0.5, 'n': 10}
# 				mover_opt = [mover1, mover2, mover3]

# 				###############################################################################################
# 				run_animation(file_opt, video_opt, mover_opt)
# 				end = time.clock()
# 				print('Finished Video Number {0} ({1}) in {2:.2f} min'.format(counter, \
# 					video_filename[:-4], (end-start)/60))
# 			counter = counter + 1