import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
from mpl_toolkits.mplot3d import Axes3D

f = h5py.File('./network/SPWR_biophysical_SPWR_biophysical_edges.h5','r')
g = h5py.File('./network/SPWR_biophysical_nodes.h5','r')

source = f['edges']['SPWR_biophysical_to_SPWR_biophysical']['source_node_id']
target = f['edges']['SPWR_biophysical_to_SPWR_biophysical']['target_node_id']

n_cells = 3375
pn_ids = np.arange(0,2767)
itn_ids = np.arange(2768,3375)

positions = g['nodes']['SPWR_biophysical']['0']['positions']
source_pos = pd.DataFrame(data=np.concatenate((np.arange(0, n_cells).reshape(-1,1), 
						positions[:,:],
						np.where(np.arange(0,n_cells)<pn_ids[-1],'PN','ITN').reshape(-1,1)),axis=1),
			  columns=['source_ID','source_x','source_y','source_z','source_type'])

target_pos = pd.DataFrame(data=np.concatenate((np.arange(0,n_cells).reshape(-1,1), 
						positions[:,:],
						np.where(np.arange(0,n_cells)<pn_ids[-1],'PN','ITN').reshape(-1,1)),axis=1),
			  columns=['target_ID','target_x','target_y','target_z','target_type'])


conns = pd.DataFrame(data=np.concatenate((source[:].reshape(-1,1),target[:].reshape(-1,1)),axis=1),
                     columns=['source_ID','target_ID'])

conns = conns.join(source_pos,on='source_ID',rsuffix='_x')
conns = conns.join(target_pos,on='target_ID',rsuffix='_x')


#print(conns[(conns.source_x.astype(int)<400)&(conns.source_x.astype(int)>200)&
#      (conns.source_y.astype(int)<400)&(conns.source_y.astype(int)>200)&
#      (conns.source_z.astype(int)<400)&(conns.source_z.astype(int)>200)&
#      (conns.source_type=='PN')]['source_ID'])


d = np.sqrt(np.sum((conns[['source_x', 'source_y', 'source_z']].values.astype(int)
	 - conns[['target_x','target_y','target_z']].values.astype(int))**2,axis=1))

conns.loc[:,'distance'] = d

conns.loc[:,'source_x'] = conns.loc[:,'source_x'].astype(int)
conns.loc[:,'source_y'] = conns.loc[:,'source_y'].astype(int)
conns.loc[:,'source_z'] = conns.loc[:,'source_z'].astype(int)

conns.loc[:,'target_x'] = conns.loc[:,'target_x'].astype(int)
conns.loc[:,'target_y'] = conns.loc[:,'target_y'].astype(int)
conns.loc[:,'target_z'] = conns.loc[:,'target_z'].astype(int)

PN2PN = conns[(conns.source_type=='PN') & (conns.target_type=='PN')]
PN2ITN = conns[(conns.source_type=='PN') & (conns.target_type=='ITN')]
ITN2PN = conns[(conns.source_type=='ITN') & (conns.target_type=='PN')]
ITN2ITN = conns[(conns.source_type=='ITN') & (conns.target_type=='ITN')]


# example connectivity scatter #
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


cell_to_plot = 772

ax.scatter(int(conns[conns.source_ID==cell_to_plot]['source_x'].values[0]),
	   int(conns[conns.source_ID==cell_to_plot]['source_y'].values[0]), 
	   int(conns[conns.source_ID==cell_to_plot]['source_z'].values[0]), 
	   marker='^',color='r')

pn2itn_x = PN2ITN[PN2ITN.source_ID==cell_to_plot]['target_x'].values
pn2itn_y = PN2ITN[PN2ITN.source_ID==cell_to_plot]['target_y'].values
pn2itn_z = PN2ITN[PN2ITN.source_ID==cell_to_plot]['target_z'].values

ax.scatter(pn2itn_x,pn2itn_y,pn2itn_z,marker='o',color='blue')

pn2pn_x = PN2PN[PN2PN.source_ID==cell_to_plot]['target_x'].values
pn2pn_y = PN2PN[PN2PN.source_ID==cell_to_plot]['target_y'].values
pn2pn_z = PN2PN[PN2PN.source_ID==cell_to_plot]['target_z'].values

ax.scatter(pn2pn_x,pn2pn_y,pn2pn_z,marker='o',color='red')

# PN2PN figure #
plt.figure()
plt.subplot(1,2,1)
density, bins = np.histogram(PN2PN['distance'], normed=True, density=True)
unity_density = density / density.sum()
widths = bins[:-1] - bins[1:]
plt.bar(bins[1:],unity_density,width=widths)
plt.title('PN2PN - pdf')
plt.xlabel('distance (um)')

plt.subplot(1,2,2)
plt.bar(bins[1:],unity_density.cumsum(),width=widths)
plt.title('PN2PN - cdf')
plt.xlabel('distance (um)')

# PN2ITN figure #
plt.figure()
plt.subplot(1,2,1)
density, bins = np.histogram(PN2ITN['distance'], normed=True, density=True)
unity_density = density / density.sum()
widths = bins[:-1] - bins[1:]
plt.bar(bins[1:],unity_density,width=widths)
plt.title('PN2ITN - pdf')
plt.xlabel('distance (um)')

plt.subplot(1,2,2)
plt.bar(bins[1:],unity_density.cumsum(),width=widths)
plt.title('PN2ITN - cdf')
plt.xlabel('distance (um)')


plt.show()

