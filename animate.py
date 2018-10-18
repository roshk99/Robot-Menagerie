import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from options import *
plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path

#This file actually generates the simulation

def run_animation(data, min_lim, max_lim, num_points):

	#Find the square that encloses all the motion
	plane_start = min(min_lim[0:2])
	plane_end = max(max_lim[0:2])

	#Initialize the 3D Figure
	fig = plt.figure(1)
	ax1 = fig.add_subplot(111, projection='3d')
	ax1.set_title(file_info['plot_title'])
	
	#Generate the square stage
	xx, yy = np.meshgrid(np.linspace(plane_start,plane_end,10), 
			np.linspace(plane_start,plane_end,10))
	zz = np.zeros((xx.shape[0], 1))
	ax1.plot_surface(xx, yy, zz, alpha=0.2)

	#Set the axis limits of the figure
	ax1.set_xlim3d(plane_start, plane_end)
	ax1.set_ylim3d(plane_start, plane_end)
	ax1.set_zlim3d(-0.1, max_lim[2])
	ax1.axis('off')

	#Set the viewpoint of the figure
	ax1.view_init(environ_opt['elevation'],environ_opt['azimuth'])
	
	#Initialize the plotting objects
	lines = []
	surfaces = []
	surfaces2 = []

	#Create a line for each path in the human trajectories
	for mover in data['human']:
		for ind, traj in enumerate(mover['trajectory']):
			lobj = ax1.plot([],[],[],lw=2, color=color_key[mover['colors'][ind]])[0]
			lines.append(lobj)

	#Create a surface for each face of the rollbot
	for mover in data['rollbot']:
		for col, verts in mover['trajectory'].items():
			surface = Poly3DCollection([], facecolors=color_key[col], edgecolors='black', 
				linewidths=1, alpha=1)
			ax1.add_collection3d(surface)
			surfaces.append(surface)

	#Create a surface for cone and bottom circle and a line for the handle 
	#for each broombot
	for mover in data['broombot']:
		for ind in range(2):
			surface2 = ax1.plot_surface(np.zeros((1,1)), np.zeros((1,1)), np.zeros((1,1)), 
				color=color_key[ind], alpha=1)
			surfaces2.append(surface2)
			surface = Poly3DCollection([], facecolors=color_key[ind], edgecolors='black', 
				linewidths=1, alpha=1)
			ax1.add_collection3d(surface)
			surfaces.append(surface)
		lobj = ax1.plot([],[],[],lw=2, color=color_key[0])[0]
		lines.append(lobj)

	#Create two lines for each armbot
	for mover in data['armbot']:
		lobj = ax1.plot([],[],[],lw=2, color=color_key[0])[0]
		lines.append(lobj)
		lobj = ax1.plot([],[],[],lw=2, color=color_key[1])[0]
		lines.append(lobj)

	#This function updates the figure for each frame i of the animation
	def animate(i):

		xlist = []
		ylist = []
		zlist = []

		cur_ind = i % file_info['num_points']
		print('{0:.2f}%'.format(cur_ind/file_info['num_points']*100))

		#Add path at frame i from the human trajectory
		for mover in data['human']:
			for path_num, traj in mover['trajectory'].items():
				x = list(traj[:,cur_ind,0])
				y = list(traj[:,cur_ind,1])
				z = list(traj[:,cur_ind,2])
				xlist.append(x)
				ylist.append(y)
				zlist.append(z)

		#Add broombot handle at frame i
		for mover in data['broombot']:
			x1 = float(mover['trajectory']['handle_points'][cur_ind,0,0,:])
			y1 = float(mover['trajectory']['handle_points'][cur_ind,0,1,:])
			z1 = float(mover['trajectory']['handle_points'][cur_ind,0,2,:])
			x2 = float(mover['trajectory']['handle_points'][cur_ind,1,0,:])
			y2 = float(mover['trajectory']['handle_points'][cur_ind,1,1,:])
			z2 = float(mover['trajectory']['handle_points'][cur_ind,1,2,:])
			xlist.append([x1, x2])
			ylist.append([y1, y2])
			zlist.append([z1, z2])

		#Add armbot handle at frame i
		for mover in data['armbot']:
			x1 = float(mover['trajectory']['handle_points'][cur_ind,0,0,:])
			y1 = float(mover['trajectory']['handle_points'][cur_ind,0,1,:])
			z1 = float(mover['trajectory']['handle_points'][cur_ind,0,2,:])
			x2 = float(mover['trajectory']['handle_points'][cur_ind,1,0,:])
			y2 = float(mover['trajectory']['handle_points'][cur_ind,1,1,:])
			z2 = float(mover['trajectory']['handle_points'][cur_ind,1,2,:])
			x3 = float(mover['trajectory']['handle_points'][cur_ind,2,0,:])
			y3 = float(mover['trajectory']['handle_points'][cur_ind,2,1,:])
			z3 = float(mover['trajectory']['handle_points'][cur_ind,2,2,:])
			xlist.append([x1, x2])
			xlist.append([x2, x3])
			ylist.append([y1, y2])
			ylist.append([y2, y3])
			zlist.append([z1, z2])
			zlist.append([z2, z3])

		#Update the data for all the lines
		for lnum,line in enumerate(lines):
			line.set_data(xlist[lnum], ylist[lnum])
			line.set_3d_properties(zlist[lnum])

		vertlist = []
		#Get the vertices at each face of the rollbot at frame i
		for mover in data['rollbot']:
			for col, verts in mover['trajectory'].items():
				tmp_verts = []
				for face in verts:
					tmp_face = []
					for point in face:
						tmp_face.append(point[cur_ind,:,:])
					tmp_verts.append(tmp_face)
				vertlist.append(tmp_verts)

		#Get the vertices for the bottom of the broombot cone at frame i 
		for mover in data['broombot']:
			for ind in range(2):
				tmp_verts = mover['trajectory']['bottom_points'][cur_ind][ind]
				vertlist.append(tmp_verts)

		#Update the data for all the faces
		for surfnum, surface in enumerate(surfaces):
			surface.set_verts(vertlist[surfnum])

		Xlist = []
		Ylist = []
		Zlist = []
		
		#Get the data for the broombot cone at frame i
		for mover in data['broombot']:
			for ind in range(2):
				X = mover['trajectory']['cone_points'][cur_ind,ind,0,:,:]
				Y = mover['trajectory']['cone_points'][cur_ind,ind,1,:,:]
				Z = mover['trajectory']['cone_points'][cur_ind,ind,2,:,:]
				Xlist.append(X)
				Ylist.append(Y)
				Zlist.append(Z)

		#Update the data for all the surfaces
		for surfnum, surface in enumerate(surfaces2):
			surface.remove()
			surface = ax1.plot_surface(Xlist[surfnum], Ylist[surfnum], Zlist[surfnum], \
				color=color_key[ind])
			surfaces2[surfnum] = surface

		return lines + surfaces + surfaces2

	#Call the animator
	anim = animation.FuncAnimation(fig, animate, range(num_points))
	FFwriter = animation.FFMpegWriter(fps=file_info['video_fps'])
	if file_info['save_video']:
		print('Starting to Save Video')
		anim.save(file_info['video_filename'], writer = FFwriter)
		print('Done Saving Video!')
	if file_info['show_animation']:
		plt.show(1)

	