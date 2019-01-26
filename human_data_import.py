from analyze_human_data import *

filename = 'mocapdata01.csv'
data_filename = 'mocapdata01'
dim_transfer = [2, 0, 1]

verticality_vec = ('WaistRBack', 'BackRight')
arm_left = ('RShoulderBack', 'RWristOut')
arm_right = ('LShoulderBack', 'LWristOut')
leg_left = ('WaistRBack', 'RAnkleOut')
leg_right = ('WaistLBack', 'LAnkleOut')

vectors = [verticality_vec, arm_left, arm_right, leg_left, leg_right]

node_traj, angles, trans_traj = analyze_human_data(filename, vectors, dim_transfer)

np.savez(data_filename, angles=angles, node_traj=node_traj, \
		trans_traj=trans_traj)
print('Saved Human Data')