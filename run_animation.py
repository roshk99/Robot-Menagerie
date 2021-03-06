import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import uniform as rrange
from matplotlib import animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

def run_animation(video_opt, mover_opt):
	#Check if the sections are all the same length
	test_length = len(mover_opt[0]['section'])
	for mover in mover_opt:
		if not len(mover['section']) == test_length:
			print('All sections must be the same length')
			return

	animation_obj = []
	for mover in mover_opt:
		#Analyze the motion capture csv file
		angles, node_traj, trans_traj = import_human_data(mover['filename'], mover['section'])

		if mover['type'] == 'human':
			mover['traj'] = generate_human_traj(node_traj, mover)
		elif mover['type'] == 'broombot':
			mover['traj'] = generate_broombot_traj(mover, angles, trans_traj)
		elif mover['type'] == 'rollbot':
			mover['traj'] = generate_rollbot_traj(mover, angles, trans_traj)
		animation_obj.append(mover)

	animate_movers(animation_obj, video_opt)

def import_human_data(filename, section):
	with np.load(filename) as f:
		angles = f['angles']
		node_traj = f['node_traj']
		trans_traj = f['trans_traj']

	angles = angles.flat[0]
	node_traj = node_traj.flat[0]

	cur_angles = {}
	for angle_name, angle in angles.items():
		cur_angles[angle_name] = {'th_x': angle['th_x'][section], \
				'th_y': angle['th_y'][section]}

	cur_node_traj = {}
	for node_name, node in node_traj.items():
		cur_node_traj[node_name] = node[section,:]

	cur_trans_traj = trans_traj[section,:]
	cur_trans_traj[:,2] = 0

	return cur_angles, cur_node_traj, cur_trans_traj

def generate_human_traj(node_traj, mover):

	#human_traj[time, path, 3 dim, 2 points]
	human_traj = np.zeros((len(mover['section']), \
		len(mover['paths']), 3, 2))

	for path_num, path in enumerate(mover['paths']):
		start_point = node_traj[path[0]] + mover['pos']
		end_point = node_traj[path[1]] + mover['pos']
		human_traj[:,path_num,:,0] = start_point + rrange(-0.01, 0.01)
		human_traj[:,path_num,:,1] = end_point + rrange(-0.01, 0.01)

	return human_traj

def generate_broombot_traj(mover, angles, trans_traj):
	num_points = angles[('WaistRBack', 'BackRight')]['th_x'].shape[0]
	if mover['vector'][0] == 'Random':
		omega_b = 1/5000
		th_x = []
		th_y = []
		for ii in range(num_points):
			A_b_x = rrange(-np.pi/2, np.pi/2)
			A_b_y = rrange(-np.pi/2, np.pi/2)
			th_x.append(A_b_x*np.sin(omega_b*ii))
			th_y.append(A_b_y*np.sin(omega_b*ii))
	else:
		th_x = angles[mover['vector']]['th_x'] + np.pi/2
		th_y = angles[mover['vector']]['th_y'] + np.pi/2
		
	#Get start and end angles for the two halves
	start_angles = [0,np.pi]
	end_angles = [np.pi, 2*np.pi]

	#Geometric properties of the broombot
	radius = mover['radius']
	height = mover['height']
	n = mover['n']

	#Initialize the three parts of the broombot
	cone_points = np.zeros((num_points, 2, 3, n, n))
	bottom_points = []
	handle_points = np.zeros((num_points, 2, 3, 1))

	#Iterating through each frame
	for ind in range(num_points):
		#Get rotation matrix for X and Y rotation by respective angles
		X_Rot = np.array([[1, 0, 0], [0, np.cos(th_x[ind]), -np.sin(th_x[ind])], 
				[0, np.sin(th_x[ind]), np.cos(th_x[ind])]])
		Y_Rot = np.array([[np.cos(th_y[ind]), 0, np.sin(th_y[ind])], [0, 1, 0], 
				[-np.sin(th_y[ind]), 0, np.cos(th_y[ind])]])
		Rot = np.matmul(X_Rot,Y_Rot)

		#Get translation trajectory for frame
		trans = np.squeeze(trans_traj[ind,:] + mover['pos'])
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
			rotX = np.reshape(newXYZ[:,0,:], (n,n)) + trans[0]
			rotY = np.reshape(newXYZ[:,1,:], (n,n)) + trans[1]
			rotZ = np.reshape(newXYZ[:,2,:], (n,n)) + trans[2]
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
				v = newXYZ[ii,:] + trans[:,np.newaxis]
				verts.append(v)
			verts = [verts]
			bottom_points[ind][half] = verts

		#Get vector for broombot handle, rotate by rotation matrix, 
		#and add to handle_points array
		v = np.array([0, 0, height*2])[:,np.newaxis]
		rot_v = np.matmul(Rot,v)
		rot_p1 = trans[:,np.newaxis]
		rot_p2 = rot_p1 + rot_v
		handle_points[ind,0,:,:] = rot_p1
		handle_points[ind,1,:,:] = rot_p2

	#Store all three parts of broombot trajectory in object
	traj = {'cone_points': cone_points, 'bottom_points': bottom_points, 
			'handle_points': handle_points}

	return traj

def generate_rollbot_traj(mover, angles, trans_traj):
	num_points = angles[('WaistRBack', 'BackRight')]['th_x'].shape[0]
	if mover['vector'][0] == 'Random':
		omega_r = 1/5000
		th = []
		for ii in range(num_points):
			A_r = rrange(-np.pi/2, np.pi/2)
			th.append(A_r*np.sin(omega_r*ii) + np.pi) 
	else:
		th = angles[mover['vector']]['th_x'] + angles[mover['vector']]['th_y']

	#Compute the 2D rotation matrix for each angle
	R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
	R = np.transpose(R, (2,0,1))

	#Get the geometric parameters of the rollbot 
	radius = mover['radius']
	stretch = mover['stretch']
	height = mover['height']
	hor_trans = trans_traj
	hor_trans[:,2] = 0
	trans = hor_trans + mover['pos']

	#Get the (x,y) vertices of the triangular prism (one half)
	p1 = np.array([radius*stretch, 0])[:,np.newaxis]
	p1 = np.matmul(R,p1) + trans[:,0:2,np.newaxis]
	p2 = np.array([-radius, radius])[:,np.newaxis]
	p2 = np.matmul(R,p2) + trans[:,0:2,np.newaxis]
	p3 = np.array([-radius, 0])[:,np.newaxis]
	p3 = np.matmul(R,p3) + trans[:,0:2,np.newaxis]

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
	p1 = np.matmul(R,p1) + trans[:,0:2,np.newaxis]
	p2 = np.array([-radius, 0])[:,np.newaxis]
	p2 = np.matmul(R,p2) + trans[:,0:2,np.newaxis]
	p3 = np.array([-radius, -radius])[:,np.newaxis]
	p3 = np.matmul(R,p3) + trans[:,0:2,np.newaxis]
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

	#Store the two halves of the triangular prism in an array (keys are color indices)
	traj = {0: verts1, 1: verts2}

	return traj

def animate_movers(animation_obj, video_opt):
	plt.rcParams['animation.ffmpeg_path'] = video_opt['ffmpeg_path']

	#Initialize the 3D Figure
	fig = plt.figure(1)
	ax1 = fig.add_subplot(111, projection='3d')
	ax1.set_title(video_opt['video_title'])

	#Generate the square stage
	xx, yy = np.meshgrid(np.linspace(video_opt['plane_start'],video_opt['plane_end'],10), 
			np.linspace(video_opt['plane_start'],video_opt['plane_end'],10))
	zz = np.zeros((xx.shape[0], 1))
	ax1.plot_surface(xx, yy, zz, alpha=0.2)

	#Set the axis limits of the figure
	ax1.set_xlim3d(video_opt['plane_start'], video_opt['plane_end'])
	ax1.set_ylim3d(video_opt['plane_start'], video_opt['plane_end'])
	ax1.set_zlim3d(-0.1, video_opt['height_max'])
	ax1.axis('off')

	#Set the viewpoint of the figure
	ax1.view_init(video_opt['elevation'],video_opt['azimuth'])

	#Initialize the plotting objects
	lines = []
	surfaces = []
	surfaces2 = []

	for mover in animation_obj:
		if mover['type'] == 'human':
			line_num = mover['traj'].shape[1]
			for line in range(line_num):
				lobj = ax1.plot([],[],[],lw=2, color=video_opt['color_key'][0])[0]
				lines.append(lobj)
		if mover['type'] == 'broombot':
			for ind in range(2):
				surface2 = ax1.plot_surface(np.zeros((1,1)), np.zeros((1,1)), np.zeros((1,1)), 
					color=video_opt['color_key'][ind], alpha=1)
				surfaces2.append(surface2)
				surface = Poly3DCollection([], facecolors=video_opt['color_key'][ind], edgecolors='black', 
					linewidths=1, alpha=1)
				ax1.add_collection3d(surface)
				surfaces.append(surface)
			lobj = ax1.plot([],[],[],lw=2, color=video_opt['color_key'][0])[0]
			lines.append(lobj)
		if mover['type'] == 'rollbot':
			for col, verts in mover['traj'].items():
				surface = Poly3DCollection([], facecolors=video_opt['color_key'][col], edgecolors='black', 
					linewidths=1, alpha=1)
				ax1.add_collection3d(surface)
				surfaces.append(surface)

	#This function updates the figure for each frame i of the animation
	def animate(i):

		if i % 300 == 0:
			print('{0:.2f}%'.format(i/len(animation_obj[0]['section'])*100))

		xlist = []
		ylist = []
		zlist = []
		vertlist = []
		xlist2 = []
		ylist2 = []
		zlist2 = []

		for mover in animation_obj:
			if mover['type'] == 'human':
				line_num = mover['traj'].shape[1]
				for path in range(line_num):
					points = mover['traj'][i,path,:,:]
					xlist.append([points[0,0], points[0,1]])
					ylist.append([points[1,0], points[1,1]])
					zlist.append([points[2,0], points[2,1]])

			if mover['type'] == 'broombot':
				x1 = float(mover['traj']['handle_points'][i,0,0,:])
				y1 = float(mover['traj']['handle_points'][i,0,1,:])
				z1 = float(mover['traj']['handle_points'][i,0,2,:])
				x2 = float(mover['traj']['handle_points'][i,1,0,:])
				y2 = float(mover['traj']['handle_points'][i,1,1,:])
				z2 = float(mover['traj']['handle_points'][i,1,2,:])
				xlist.append([x1, x2])
				ylist.append([y1, y2])
				zlist.append([z1, z2])

				for ind in range(2):
					tmp_verts = mover['traj']['bottom_points'][i][ind]
					vertlist.append(tmp_verts)

				for ind in range(2):
					X = mover['traj']['cone_points'][i,ind,0,:,:]
					Y = mover['traj']['cone_points'][i,ind,1,:,:]
					Z = mover['traj']['cone_points'][i,ind,2,:,:]
					xlist2.append(X)
					ylist2.append(Y)
					zlist2.append(Z)

			if mover['type'] == 'rollbot':
				for col, verts in mover['traj'].items():
					tmp_verts = []
					for face in verts:
						tmp_face = []
						for point in face:
							tmp_face.append(point[i,:,:])
						tmp_verts.append(tmp_face)
					vertlist.append(tmp_verts)

		#Update the data for all the lines
		for lnum,line in enumerate(lines):
			line.set_data(xlist[lnum], ylist[lnum])
			line.set_3d_properties(zlist[lnum])

		#Update the data for all the faces
		for surfnum, surface in enumerate(surfaces):
			surface.set_verts(vertlist[surfnum])

		if video_opt['img_flag']:
			plt.savefig(str(i)+".png", dpi=300)

		#Update the data for all the surfaces
		for surfnum, surface in enumerate(surfaces2):
			surface.remove()
			surface = ax1.plot_surface(xlist2[surfnum], ylist2[surfnum], zlist2[surfnum], \
				color=video_opt['color_key'][ind])
			surfaces2[surfnum] = surface

		return lines + surfaces + surfaces2

	#Call the animator
	if video_opt['save_type'] == 'video':
		anim = animation.FuncAnimation(fig, animate, range(len(animation_obj[0]['section'])))
		FFwriter = animation.FFMpegWriter(fps=video_opt['video_fps'])
		anim.save(video_opt['video_filename'], writer = FFwriter)
		plt.close(fig)
	else:
		step = int(np.floor(len(animation_obj[0]['section'])*video_opt['animation_speed']))
		anim = animation.FuncAnimation(fig, animate, \
			range(0, len(animation_obj[0]['section']), step))
	plt.show()

