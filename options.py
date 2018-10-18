import numpy as np

#Mocap file options
start_ind = 0
end_ind = 3000
filename = 'mocapdata01.csv'

#Animation Options
show_animation = False

#Video Options
video_filename = 'test1.mp4'
video_flag = False
video_title = 'Test1'
video_fps = 60

#Angle Plot Options
plot_angles = False
plot_title = 'test1'

#List of Movers
mover_specs = [['human', np.array([[0,0,0]]), ['angle', 'vert']], \
				['rollbot', np.array([[0,-1.5,0]]), ['angle', 'shoulder_hand_right']], \
				['broombot', np.array([[0,-3,0]]), ['angle', 'shoulder_elbow_right']] ]


###############################################################################################

#FFMPEG path
ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg'

#CSV File Info
file_info = {'filename': filename, 'section': range(start_ind,end_ind), \
		'num_points': int(np.floor((end_ind-start_ind)*0.5)), 'save_video': video_flag, \
		'video_filename': video_filename, 'show_animation': show_animation, \
		'plot_title': plot_title, 'plot_angles': plot_angles, 'plot_title': plot_title, \
		'video_fps': video_fps}

#Plotting Options
environ_opt = {'floor_offset': 1, 'vertical_offset': 0.5, 'elevation': 31, 'azimuth': -180}

#MoCap Skeleton Plotting Options
paths = {(4,8): 0, (5,6): 1, (2,3): 0, (22,23,20,19,4,6,3,32,34,36): 0, \
		(15,16,12,4,5,2,26,28,30):1}

#Colors of the simulations
color_key = ['green', 'red']

#Mo-Cap Axes to World Axes
dim_transfer = [2, 0, 1]

#Geometry parameters for
geometry_specs = {'human': {}, 'rollbot': {'radius': 0.25, 'height': 0.2, 'stretch': 1.5},
					'broombot': {'radius': 0.25, 'height': 0.5, 'n': 10},
					'armbot': {'height': 0.3}}

movers = []
for mover_type, mover_pos, mover_motion_type in mover_specs:
	movers.append({'offset': mover_pos, 'type': mover_type, 
			'motion_type': mover_motion_type, 'geometry': geometry_specs[mover_type]})
	
