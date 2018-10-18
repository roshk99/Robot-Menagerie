from analyze_human_data import analyze_human_data
from options import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from animate import run_animation
from random import uniform as rrange

#Running this file with options specified in options.py will generate a simulation 
#of movers on a stage

def main():
	#Analyze the motion capture csv file
	human_data_obj = analyze_human_data(file_info)

	#Generate the trajectories for each of the movers
	mover_objs = list([])
	for mover in movers:
		if mover['type'] == 'human':
			traj_obj = generate_human_trajectory(mover, human_data_obj)
		elif mover['type'] == 'rollbot':
			traj_obj = generate_rollbot_trajectory(mover, human_data_obj)
		elif mover['type'] == 'broombot':
			traj_obj = generate_broombot_trajectory(mover, human_data_obj)
		elif mover['type'] == 'armbot':
			traj_obj = generate_armbot_trajectory(mover, human_data_obj)
		mover_objs.append(traj_obj)

	#Animate the movers
	animate_movers(mover_objs, human_data_obj['num_points'])

	#Generate angle plots
	if file_info['plot_angles']:
		plot_angles(human_data_obj, ['back_waist_right', 'head_neck', 'head_waist_right'], \
			file_info['plot_title'] + '_verticality')
		plot_angles(human_data_obj, ['shoulder_hand_right', 'shoulder_elbow_right', 'elbow_hand_right'], \
			file_info['plot_title'] + '_rightupper')
		plot_angles(human_data_obj, ['waist_ankle_right', 'waist_knee_right', 'knee_ankle_right'], \
			file_info['plot_title'] + '_rightlower')
		plot_angles(human_data_obj, ['shoulder_hand_left', 'shoulder_elbow_left', 'elbow_hand_left'], \
			file_info['plot_title'] + '_leftupper')
		plot_angles(human_data_obj, ['waist_ankle_left', 'waist_knee_left', 'knee_ankle_left'], \
			file_info['plot_title'] + '_leftlower')

def generate_human_trajectory(mover, human_data_obj):
	#Get the axis limits of the human movement
	max_lim = np.amax(np.amax(human_data_obj['trajectories'], axis=0), axis=0) \
			+ mover['offset']
	min_lim = np.amin(np.amin(human_data_obj['trajectories'], axis=0), axis=0) \
			+ mover['offset']

	#The trajectory object is indexed by: trajectory[path number][node in the path]
	#[x, y, or z ][1]
	trajectory = {}
	colors = []
	path_count = 0

	#For each path (or continous sequence of segments in skeleton)
	for path, color in human_data_obj['paths'].items():
		node_count = 0
		traj = np.zeros([len(path), file_info['num_points'], 3])

		#Append the trajectories of each node in the path
		for node in path:
			traj[node_count, :, :] = human_data_obj['trajectories'][node, :, :] \
				+ mover['offset']
			node_count = node_count + 1
		trajectory[path_count] = traj

		#Store the color of the path
		colors.append(color)
		path_count = path_count + 1

	#Add variables to an object
	result = {'trajectory': trajectory, 'colors': colors, 'min_lim': min_lim, 
				'max_lim': max_lim, 'type': 'human'}
	return result

def generate_rollbot_trajectory(mover, human_data_obj):
	trans_traj = (human_data_obj['trans_traj'] + mover['offset'])[:,:2]

	if mover['motion_type'][0] == 'angle':
		#Get the translation and the single angle
		angles = human_data_obj[mover['motion_type'][1]]
		th = angles['comb_th'] - np.pi
	if mover['motion_type'][0] == 'random':
		if mover['motion_type'][1] == 'periodic':
			scaling_fac = float(human_data_obj['orig_num_points'])/human_data_obj['num_points']
			omega_r = scaling_fac/5000
			th = []
			for ii in range(human_data_obj['num_points']):
				A_r = rrange(-np.pi/2, np.pi/2)
				th.append(A_r*np.sin(omega_r*ii) + np.pi)

	#Compute the 2D rotation matrix for each angle
	R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
	R = np.transpose(R, (2,0,1))
	
	#Get the geometric parameters of the rollbot 
	radius = mover['geometry']['radius']
	stretch = mover['geometry']['stretch']
	height = mover['geometry']['height']
	
	#Get the (x,y) vertices of the triangular prism (one half)
	p1 = np.array([radius*stretch, 0])[:,np.newaxis]
	p1 = np.matmul(R,p1) + trans_traj[:,:,np.newaxis]
	p2 = np.array([-radius, radius])[:,np.newaxis]
	p2 = np.matmul(R,p2) + trans_traj[:,:,np.newaxis]
	p3 = np.array([-radius, 0])[:,np.newaxis]
	p3 = np.matmul(R,p3) + trans_traj[:,:,np.newaxis]

	#Get the z value for the top and bottom
	low_z = np.zeros((p1.shape[0], 1, 1))
	high_z = height*np.ones((p1.shape[0], 1, 1))
	
	#Get all 6 3d points
	p1_low = np.concatenate((p1,low_z), axis=1)
	p1_high = np.concatenate((p1,high_z), axis=1)
	p2_low = np.concatenate((p2,low_z), axis=1)
	p2_high = np.concatenate((p2,high_z), axis=1)
	p3_low = np.concatenate((p3,low_z), axis=1)
	p3_high = np.concatenate((p3,high_z), axis=1)

	#Store the vertices of faces in an array
	verts1 = [ [p1_low, p2_low, p3_low], [p1_high, p2_high, p3_high], 
			[p1_low, p1_high, p2_high, p1_low], [p1_low, p1_high, p3_high, p3_low], 
			[p2_low, p2_high, p3_high, p3_low]]

	#Get the (x,y) vertices of the triangular prism (other half)
	p1 = np.array([radius*stretch, 0])[:,np.newaxis]
	p1 = np.matmul(R,p1) + trans_traj[:,:,np.newaxis]
	p2 = np.array([-radius, 0])[:,np.newaxis]
	p2 = np.matmul(R,p2) + trans_traj[:,:,np.newaxis]
	p3 = np.array([-radius, -radius])[:,np.newaxis]
	p3 = np.matmul(R,p3) + trans_traj[:,:,np.newaxis]
	low_z = np.zeros((p1.shape[0], 1, 1))
	
	#Get all 6 3d points
	p1_low = np.concatenate((p1,low_z), axis=1)
	p1_high = np.concatenate((p1,high_z), axis=1)
	p2_low = np.concatenate((p2,low_z), axis=1)
	p2_high = np.concatenate((p2,high_z), axis=1)
	p3_low = np.concatenate((p3,low_z), axis=1)
	p3_high = np.concatenate((p3,high_z), axis=1)
	
	#Store the vertices of faces in an array
	verts2 = [ [p1_low, p2_low, p3_low], [p1_high, p2_high, p3_high], 
			[p1_low, p1_high, p2_high, p1_low], [p1_low, p1_high, p3_high, p3_low], 
			[p2_low, p2_high, p3_high, p3_low]]

	#Find the bounds of the rollbot movement in (x,y) direction
	max_lim = np.amax(trans_traj, axis=0) + 2*stretch*np.array([radius, radius])
	min_lim = np.amin(trans_traj, axis=0) - 2*stretch*np.array([radius, radius])

	#Add z component to the limits
	max_lim = np.concatenate((max_lim, np.array([height])), axis=0)
	min_lim = np.concatenate((min_lim, np.array([0])), axis=0)

	#Store the two halves of the triangular prism in an array (keys are color indices)
	traj = {0: verts1, 1: verts2}

	#Add variables to an array
	result = {'trajectory': traj, 'min_lim': min_lim, 'max_lim': max_lim, 'type': 'rollbot'}
	return result

def generate_broombot_trajectory(mover, human_data_obj):

	trans_trajs = (np.concatenate((human_data_obj['trans_traj'][:,:2], 
			np.zeros((human_data_obj['num_points'], 1))), axis=1) + mover['offset'])

	if mover['motion_type'][0] == 'angle':
		#Get the two angles and the translation trajectory (only taking x and y component)
		angles = human_data_obj[mover['motion_type'][1]]
		th_x = angles['th_x'] + np.pi/2
		th_y = angles['th_y'] + np.pi/2
	if mover['motion_type'][0] == 'random':
		if mover['motion_type'][1] == 'periodic':
			scaling_fac = float(human_data_obj['orig_num_points'])/human_data_obj['num_points']
			omega_b = scaling_fac/5000
			th_x = []
			th_y = []
			for ii in range(human_data_obj['num_points']):
				A_b_x = rrange(-np.pi/2, np.pi/2)
				A_b_y = rrange(-np.pi/2, np.pi/2)
				th_x.append(A_b_x*np.sin(omega_b*ii))
				th_y.append(A_b_y*np.sin(omega_b*ii))
				
	#Get start and end angles for the two halves
	start_angles = [0,np.pi]
	end_angles = [np.pi, 2*np.pi]

	#Geometric properties of the broombot
	radius = mover['geometry']['radius']
	height = mover['geometry']['height']
	n = mover['geometry']['n']

	#Initialize the three parts of the broombot
	cone_points = np.zeros((human_data_obj['num_points'], 2, 3, n, n))
	bottom_points = []
	handle_points = np.zeros((human_data_obj['num_points'], 2, 3, 1))

	#Iterating through each frame
	for ind in range(human_data_obj['num_points']):
		#Get rotation matrix for X and Y rotation by respective angles
		X_Rot = np.array([[1, 0, 0], [0, np.cos(th_x[ind]), -np.sin(th_x[ind])], 
				[0, np.sin(th_x[ind]), np.cos(th_x[ind])]])
		Y_Rot = np.array([[np.cos(th_y[ind]), 0, np.sin(th_y[ind])], [0, 1, 0], 
				[-np.sin(th_y[ind]), 0, np.cos(th_y[ind])]])
		Rot = np.matmul(X_Rot,Y_Rot)

		#Get translation trajectory for frame
		trans_traj = trans_trajs[ind,:]
		trans_traj = np.reshape(trans_traj, (3))

		bottom_points.append({})

		#For each half of the the broombot
		for half in range(2):

			#Get range of radii and angles for cone points
			th1 = np.linspace(start_angles[half], end_angles[half], n)
			r1 = np.linspace(0, radius, n)
			R, TH = np.meshgrid(r1, th1)

			#Get x, y, and z points for the cone
			Z = -R + radius
			X = R*np.cos(TH)
			Y = R*np.sin(TH)
			newX = np.reshape(X, (n*n,1))
			newY = np.reshape(Y, (n*n,1))
			newZ = np.reshape(Z, (n*n,1))
			XYZ = np.concatenate((newX[:,np.newaxis:], newY[:,np.newaxis:], 
				newZ[:,np.newaxis:]), axis=1)[:,:,np.newaxis]

			#Rotate the points with the rotation matrix and add to cone_points object
			newXYZ = np.matmul(Rot,XYZ)
			rotX = np.reshape(newXYZ[:,0,:], (n,n)) + trans_traj[0]
			rotY = np.reshape(newXYZ[:,1,:], (n,n)) + trans_traj[1]
			rotZ = np.reshape(newXYZ[:,2,:], (n,n)) + trans_traj[2]
			cone_points[ind,half,0,:,:] = rotX
			cone_points[ind,half,1,:,:] = rotY
			cone_points[ind,half,2,:,:] = rotZ

			#For the bottom of the cone (just a circle), repeat the same process as above
			r2 = radius
			X = r2*np.cos(th1)[:,np.newaxis]
			Y = r2*np.sin(th1)[:,np.newaxis]
			Z = np.zeros(n)[:,np.newaxis]
			XYZ = np.concatenate((X,Y,Z),axis=1)[:,:,np.newaxis]

			#Rotate the bottom points with the rotation matrix and add to bottom_points object
			newXYZ = np.matmul(Rot,XYZ)
			verts = []
			for ii in range(n):
				v = newXYZ[ii,:] + trans_traj[:,np.newaxis]
				verts.append(v)
			verts = [verts]
			bottom_points[ind][half] = verts

		#Get vector for broombot handle, rotate by rotation matrix, 
		#and add to handle_points array
		v = np.array([0, 0, height*2])[:,np.newaxis]
		rot_v = np.matmul(Rot,v)
		rot_p1 = trans_traj[:,np.newaxis]
		rot_p2 = rot_p1 + rot_v
		handle_points[ind,0,:,:] = rot_p1
		handle_points[ind,1,:,:] = rot_p2

	#Store all three parts of broombot trajectory in object
	traj = {'cone_points': cone_points, 'bottom_points': bottom_points, 
			'handle_points': handle_points}

	#Get limits of motion
	max_lim = np.amax(trans_trajs, axis=0) + height*3*np.array([1,1,1])
	min_lim = np.amin(trans_trajs, axis=0) - height*3*np.array([1,1,1])

	#Add variables to array
	result = {'trajectory': traj, 'min_lim': min_lim, 'max_lim': max_lim, \
			'type': 'broombot'}
	return result

def generate_armbot_trajectory(mover, human_data_obj):
	trans_trajs = (np.concatenate((human_data_obj['trans_traj'][:,:2], 
			np.zeros((human_data_obj['num_points'], 1))), axis=1) + mover['offset'])

	if mover['motion_type'][0] == 'angle':
		angles_lower = human_data_obj[mover['motion_type'][1]]
		th_x_lower = angles_lower['th_x'] + np.pi/2
		th_y_lower = angles_lower['th_y'] + np.pi/2
		angles_upper = human_data_obj[mover['motion_type'][2]]
		th_x_upper = angles_upper['th_x'] + np.pi/2
		th_y_upper = angles_upper['th_y'] + np.pi/2

	#Geometric properties of the broombot
	height = mover['geometry']['height']

	#Initialize the three points
	handle_points = np.zeros((human_data_obj['num_points'], 3, 3, 1))

	#Iterating through each frame
	for ind in range(human_data_obj['num_points']):
		#Get rotation matrix for X and Y rotation by respective angles
		X_Rot_lower = np.array([[1, 0, 0], 
				[0, np.cos(th_x_lower[ind]), -np.sin(th_x_lower[ind])], 
				[0, np.sin(th_x_lower[ind]), np.cos(th_x_lower[ind])]])
		Y_Rot_lower = np.array([[np.cos(th_y_lower[ind]), 0, np.sin(th_y_lower[ind])], 
				[0, 1, 0], 
				[-np.sin(th_y_lower[ind]), 0, np.cos(th_y_lower[ind])]])
		Rot_lower = np.matmul(X_Rot_lower,Y_Rot_lower)

		X_Rot_upper = np.array([[1, 0, 0], 
				[0, np.cos(th_x_upper[ind]), -np.sin(th_x_upper[ind])], 
				[0, np.sin(th_x_upper[ind]), np.cos(th_x_upper[ind])]])
		Y_Rot_upper = np.array([[np.cos(th_y_upper[ind]), 0, np.sin(th_y_upper[ind])], 
				[0, 1, 0], 
				[-np.sin(th_y_upper[ind]), 0, np.cos(th_y_upper[ind])]])
		Rot_upper = np.matmul(X_Rot_upper,Y_Rot_upper)

		#Get translation trajectory for frame
		trans_traj = trans_trajs[ind,:]
		trans_traj = np.reshape(trans_traj, (3))

		#Get vector for lower part
		v_lower = np.array([0, 0, height*2])[:,np.newaxis]
		rot_v_lower = np.matmul(Rot_lower,v_lower)
		rot_p1_lower = trans_traj[:,np.newaxis]
		rot_p2_lower = rot_p1_lower + rot_v_lower
		handle_points[ind,0,:,:] = rot_p1_lower
		handle_points[ind,1,:,:] = rot_p2_lower

		#Get vector for upper part
		v_upper = np.array([0, 0, height*2])[:,np.newaxis]
		rot_v_upper = np.matmul(Rot_upper,v_upper)
		rot_p1_upper = rot_p2_lower
		rot_p2_upper = rot_p1_upper + rot_v_upper
		handle_points[ind,2,:,:] = rot_p2_upper
		
	#Store all three parts of armbot trajectory in object
	traj = {'handle_points': handle_points}

	#Get limits of motion
	max_lim = np.amax(trans_trajs, axis=0) + height*6*np.array([1,1,1])
	min_lim = np.amin(trans_trajs, axis=0) - height*6*np.array([1,1,1])

	#Add variables to array
	result = {'trajectory': traj, 'min_lim': min_lim, 'max_lim': max_lim, \
			'type': 'armbot'}
	return result

def animate_movers(mover_objs, num_points):

	#Find the minimum and maximum of motion limits from all movers
	min_lims = np.empty([len(mover_objs), 3])
	max_lims = np.empty([len(mover_objs), 3])
	mover_count = 0
	for mover in mover_objs:
		min_lims[mover_count, :] = mover['min_lim']
		max_lims[mover_count, :] = mover['max_lim']
		mover_count = mover_count + 1

	#Add floor and vertical offset to axis limits
	min_lim = np.amin(min_lims, axis=0) \
			- np.array([environ_opt['floor_offset'],environ_opt['floor_offset'],0])
	max_lim = np.amax(max_lims, axis=0) + np.array([environ_opt['floor_offset'], \
		environ_opt['floor_offset'],environ_opt['vertical_offset']])
	
	#Store each mover object based on type
	animation_obj = {}
	animation_obj['human'] = []
	animation_obj['rollbot'] = []
	animation_obj['broombot'] = []
	animation_obj['armbot'] = []
	for mover in mover_objs:
		if mover['type'] == 'human':
			animation_obj['human'].append(mover)
		if mover['type'] == 'rollbot':
			animation_obj['rollbot'].append(mover)
		if mover['type'] == 'broombot':
			animation_obj['broombot'].append(mover)
		if mover['type'] == 'armbot':
			animation_obj['armbot'].append(mover)

	#Run the animation
	run_animation(animation_obj, min_lim, max_lim, num_points)

def plot_angles(human_data_obj, angle_names, angle_plot_name):
	fig = plt.figure()

	th_x_vec = []
	th_y_vec = []
	comb_th_vec = []
	for name in angle_names:
		th_x_vec.append(human_data_obj[name]['th_x'])
		th_y_vec.append(human_data_obj[name]['th_y'])
		comb_th_vec.append(human_data_obj[name]['comb_th'])

	t = human_data_obj['time']
	ax3 = plt.subplot(313)
	for line in comb_th_vec:
		plt.plot(t, line*180.0/np.pi)
	plt.setp(ax3.get_xticklabels(), fontsize=8)
	plt.grid(b=True)
	ax3.set_xlabel('Time (s)')
	ax3.set_ylabel('Comb Th (deg)')

	ax2 = plt.subplot(312, sharex=ax3)
	for line in th_y_vec:
		plt.plot(t, line*180.0/np.pi)
	plt.setp(ax2.get_xticklabels(), visible=False)
	plt.grid(b=True)
	ax2.set_ylabel('Theta Y (deg)')

	ax1 = plt.subplot(311, sharex=ax3)
	for line in th_x_vec:
		plt.plot(t, line*180.0/np.pi)
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.grid(b=True)
	ax1.legend(angle_names)
	ax1.set_ylabel('Theta X (deg)')
	ax1.set_title(file_info['plot_title'])
	#plt.show()

	plt.savefig(angle_plot_name)
main()

