import csv
import numpy as np
from numpy import linalg as LA

#This file is used to analyze the csv file output from OptiTrack and 
#compute the verticality metrics

def analyze_human_data(filename, vectors, dim_transfer):
	#Process csv file
	node_traj = get_raw_data(filename, dim_transfer)
	
	#Get Angles
	angles = {}
	for vector_name in vectors:
		vector = node_traj[vector_name[1]] \
				-node_traj[vector_name[0]]
		th_x, th_y = find_angles(vector)
		angles[vector_name] = {'th_x': th_x, 'th_y': th_y}
		
	#Get the translation node trajectory
	trans_traj = node_traj['BackTop']	

	return node_traj, angles, trans_traj

def get_raw_data(filename, dim_transfer):
	with open(filename, 'r') as csvfile:
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
				time = np.zeros(frame_num)
			#Get Node Names
			if row_count == 3:
				node_names = row[2::3]
				node_num = int(len(node_names))
				trajectories = np.zeros((node_num, frame_num, 3))
			#Get Time and Trajectories
			if row_count >= 7:	
				entry = 2
				for node in range(node_num):
					#Check for blank cells
					for dim in range(3):
						if row[entry] == '':
							row[entry] = np.nan
						trajectories[node,frame,dim] = float(row[entry])
						entry = entry + 1
				frame = frame + 1				
			row_count = row_count + 1

	#Remove frames where mocap system drops the signal of one or more markers
	num_points = time.size
	smooth_trajectories = trajectories
	for node in range(node_num):
		mat = trajectories[node,:,:]
		interp_mat = interpolate_nans(mat)
		smooth_trajectories[node,:,:] = interp_mat

	#Save trajectories
	node_trajectories = {}
	split_ind = node_names[0].find(':') + 1
	for ind in range(node_num):
		name = node_names[ind][split_ind:]
		node_trajectories[name] = smooth_trajectories[ind,:,dim_transfer].T
	return node_trajectories

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
	#comb_th = LA.norm(np.concatenate((th_x[:,np.newaxis], th_y[:,np.newaxis]), axis=1), axis=1)
	
	return (th_x, th_y)

def interpolate_nans(X):
    """Overwrite NaNs with column value interpolations."""
    for j in range(X.shape[1]):
        mask_j = np.isnan(X[:,j])
        X[mask_j,j] = np.interp(np.flatnonzero(mask_j), np.flatnonzero(~mask_j), X[~mask_j,j])
    return X


		
