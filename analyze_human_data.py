import csv
import numpy as np
from numpy import linalg as LA
from options import *

#This file is used to analyze the csv file output from OptiTrack and 
#compute the verticality metrics

def analyze_human_data(file_info):
	#Process csv file
	human_data_obj = get_raw_data(file_info)

	#Get the relevant node trajectories
	waist_right_node_num = human_data_obj['node_names'].index('Skel01:WaistRBack')
	back_right_node_num = human_data_obj['node_names'].index('Skel01:BackRight')
	waist_left_node_num = human_data_obj['node_names'].index('Skel01:WaistLBack')
	back_left_node_num = human_data_obj['node_names'].index('Skel01:BackLeft')
	head_node_num = human_data_obj['node_names'].index('Skel01:HeadTop')
	neck_node_num = human_data_obj['node_names'].index('Skel01:BackTop')
	shoulder_right_node_num = human_data_obj['node_names'].index('Skel01:RShoulderTop')
	elbow_right_node_num = human_data_obj['node_names'].index('Skel01:RElbowOut')
	hand_right_node_num = human_data_obj['node_names'].index('Skel01:RHandOut')
	knee_right_node_num = human_data_obj['node_names'].index('Skel01:RKneeOut')
	ankle_right_node_num = human_data_obj['node_names'].index('Skel01:RAnkleOut')
	shoulder_left_node_num = human_data_obj['node_names'].index('Skel01:LShoulderTop')
	elbow_left_node_num = human_data_obj['node_names'].index('Skel01:LElbowOut')
	hand_left_node_num = human_data_obj['node_names'].index('Skel01:LHandOut')
	knee_left_node_num = human_data_obj['node_names'].index('Skel01:LKneeOut')
	ankle_left_node_num = human_data_obj['node_names'].index('Skel01:LAnkleOut')

	#Core Vectors
	v_back_waist_right = human_data_obj['trajectories'][back_right_node_num,:,:] \
			- human_data_obj['trajectories'][waist_right_node_num,:,:]
	v_head_neck = human_data_obj['trajectories'][head_node_num,:,:] \
			- human_data_obj['trajectories'][neck_node_num,:,:]
	v_head_waist_right = human_data_obj['trajectories'][head_node_num,:,:] \
			- human_data_obj['trajectories'][waist_right_node_num,:,:]
	v_back_waist_left = human_data_obj['trajectories'][back_left_node_num,:,:] \
			- human_data_obj['trajectories'][waist_left_node_num,:,:]
	v_head_waist_left = human_data_obj['trajectories'][head_node_num,:,:] \
			- human_data_obj['trajectories'][waist_left_node_num,:,:]

	#Upper Body Vectors
	v_shoulder_hand_right = human_data_obj['trajectories'][shoulder_right_node_num,:,:] \
			- human_data_obj['trajectories'][hand_right_node_num,:,:]
	v_shoulder_elbow_right = human_data_obj['trajectories'][shoulder_right_node_num,:,:] \
			- human_data_obj['trajectories'][elbow_right_node_num,:,:]
	v_elbow_hand_right = human_data_obj['trajectories'][elbow_right_node_num,:,:] \
			- human_data_obj['trajectories'][hand_right_node_num,:,:]
	v_shoulder_hand_left = human_data_obj['trajectories'][shoulder_left_node_num,:,:] \
			- human_data_obj['trajectories'][hand_left_node_num,:,:]
	v_shoulder_elbow_left = human_data_obj['trajectories'][shoulder_left_node_num,:,:] \
			- human_data_obj['trajectories'][elbow_left_node_num,:,:]
	v_elbow_hand_left = human_data_obj['trajectories'][elbow_left_node_num,:,:] \
			- human_data_obj['trajectories'][hand_left_node_num,:,:]

	#Lower Body Vectors
	v_waist_ankle_right = human_data_obj['trajectories'][waist_right_node_num,:,:] \
			- human_data_obj['trajectories'][ankle_right_node_num,:,:]
	v_waist_knee_right = human_data_obj['trajectories'][waist_right_node_num,:,:] \
			- human_data_obj['trajectories'][knee_right_node_num,:,:]
	v_knee_ankle_right = human_data_obj['trajectories'][knee_right_node_num,:,:] \
			- human_data_obj['trajectories'][ankle_right_node_num,:,:]
	v_waist_ankle_left = human_data_obj['trajectories'][waist_left_node_num,:,:] \
			- human_data_obj['trajectories'][ankle_left_node_num,:,:]
	v_waist_knee_left = human_data_obj['trajectories'][waist_left_node_num,:,:] \
			- human_data_obj['trajectories'][knee_left_node_num,:,:]
	v_knee_ankle_left = human_data_obj['trajectories'][knee_left_node_num,:,:] \
			- human_data_obj['trajectories'][ankle_left_node_num,:,:]

	vector_names = ['back_waist_right', 'head_neck', 'head_waist_right',  \
			'shoulder_hand_right','shoulder_elbow_right', 'elbow_hand_right', \
			'waist_ankle_right', 'waist_knee_right', 'knee_ankle_right', 'back_waist_left', \
			'shoulder_hand_left','shoulder_elbow_left', 'elbow_hand_left', \
			'waist_ankle_left', 'waist_knee_left', 'knee_ankle_left',]
	vector_values = [v_back_waist_right, v_head_neck, v_head_waist_right, \
			 v_shoulder_hand_right, v_shoulder_elbow_right, v_elbow_hand_right, \
			 v_waist_ankle_right, v_waist_knee_right, v_knee_ankle_right, v_back_waist_left, \
			 v_shoulder_hand_left, v_shoulder_elbow_left, v_elbow_hand_left, \
			 v_waist_ankle_left, v_waist_knee_left, v_knee_ankle_left,]
			
	for name, value in zip(vector_names, vector_values):
		(th_x, th_y, comb_th) = find_angles(value)
		human_data_obj[name] = {'th_x': th_x, 'th_y': th_y, 'comb_th': comb_th}

	#Get the translation node trajectory
	trans_node_num = human_data_obj['node_names'].index('Skel01:BackTop')
	trans_traj = human_data_obj['trajectories'][trans_node_num,:,:]
	
	human_data_obj['trans_traj'] = trans_traj
	human_data_obj['paths'] = paths
	
	return human_data_obj

def get_raw_data(file_info):
	with open(file_info['filename'], 'r') as csvfile:
		reader = csv.reader(csvfile)
		row_count = 0
		frame = 0
		for row in reader:
			#Get Recording Global Information
			if row_count == 0:
				frame_rate = float(row[5])
				frame_num = int(row[11])
				rotation_type = row[13]
				units = row[15]
				time = np.zeros(len(file_info['section']))
			#Get Node Names
			if row_count == 3:
				node_names = row[2::3]
				node_num = int(len(node_names))
				trajectories = np.zeros((node_num, len(file_info['section']), 3))
			#Get Time and Trajectories
			if row_count >= 7:	
				entry = 2
				for node in range(node_num):
					#Check for blank cells
					for dim in range(3):
						if row[entry] == '':
							row[entry] = 0.0
						#Only add the frames in the desired section
						if frame in file_info['section']:
							ind = file_info['section'].index(frame)
							time[ind] = float(row[1])
							trajectories[node,ind,dim] = float(row[entry])
						entry = entry + 1
				frame = frame + 1				
			row_count = row_count + 1

	#Remove frames where mocap system drops the signal of one or more markers
	error_points = set()
	for node in range(node_num):
		for dim in range(3):
			ind = list(np.where(trajectories[node,:,dim] == 0)[0])
			error_points.update(ind)
	trajectories = np.delete(trajectories, list(error_points), 1)
	time = np.delete(time, list(error_points))
	orig_num_points = time.size

	#Interpolate to desired number of points
	interp_time = np.interp(np.linspace(0, orig_num_points, file_info['num_points']), 
					range(0,orig_num_points), time)
	interp_trajectories = np.zeros((node_num, file_info['num_points'], 3))
	for node in range(node_num):
		for dim in range(3):
			interp_trajectories[node,:,dim] = np.interp(interp_time[:], time[:], 
				trajectories[node,:,dim_transfer[dim]])

	#Add variables to object
	obj = {'num_points': file_info['num_points'], 'frame_rate': frame_rate, \
			'frame_num': frame_num, 'rotation_type': rotation_type, 'units': units, \
			'time': interp_time, 'node_names': node_names, 'node_num': node_num, \
			'trajectories': interp_trajectories, 'orig_num_points': orig_num_points}
	return obj

def find_angles(v):
	#Get normalized vector v
	num_points = len(v)
	v_norm = LA.norm(v, axis=1)
	v_normalized = np.divide(v,np.repeat(v_norm[:,np.newaxis], 3, axis=1))
	
	#Unit vectors in x, y, and z directions
	unit_x = np.repeat(np.array([[1, 0, 0]]), num_points, axis=0)
	unit_y = np.repeat(np.array([[0, 1, 0]]), num_points, axis=0)
	unit_z = np.repeat(np.array([[0, 0, 1]]), num_points, axis=0)
	
	#Get the projection of v onto the xz and yz planes
	v_x = np.cross(unit_x, np.cross(v, unit_x))
	v_x_norm = LA.norm(v_x, axis=1)
	v_x_normalized = np.divide(v_x,np.repeat(v_x_norm[:,np.newaxis], 3, axis=1))
	v_y = np.cross(unit_y, np.cross(v, unit_y))
	v_y_norm = LA.norm(v_y, axis=1)
	v_y_normalized = np.divide(v_y,np.repeat(v_y_norm[:,np.newaxis], 3, axis=1))

	#Compute the angle between the unit z vector and each of the projects
	v_x_dot = np.sum(np.multiply(unit_z, v_x_normalized), axis=1)
	v_y_dot = np.sum(np.multiply(unit_z, v_y_normalized), axis=1)

	th_x = np.arccos(v_x_dot) - np.pi/2
	th_y = np.arccos(v_y_dot) - np.pi/2
	
	#Get the norm of the x and y angles for the combined angle
	comb_th = LA.norm(np.concatenate((th_x[:,np.newaxis], th_y[:,np.newaxis]), axis=1), axis=1)
	
	return (th_x, th_y, comb_th)



		
