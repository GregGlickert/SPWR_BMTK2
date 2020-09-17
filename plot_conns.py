import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb

f = h5py.File('SPWR_biophysical_SPWR_biophysical_edges.h5','r')
g = h5py.File('SPWR_biophysical_nodes.h5','r')

source = f['edges']['SPWR_biophysical_SPWR_biophysical']['source_node_id']
target = f['edges']['SPWR_biophysical_SPWR_biophysical']['target_node_id']


positions = g['nodes']['SPWR_biophysical']['0']['positions']
source_pos = pd.DataFrame(data=np.concatenate((np.arange(0,27000).reshape(-1,1), 
						positions[:,:],
						np.where(np.arange(0,27000)<22140,'PN','ITN').reshape(-1,1)),axis=1),
			  columns=['source_ID','source_x','source_y','source_z','source_type'])

target_pos = pd.DataFrame(data=np.concatenate((np.arange(0,27000).reshape(-1,1), 
						positions[:,:],
						np.where(np.arange(0,27000)<22140,'PN','ITN').reshape(-1,1)),axis=1),
			  columns=['target_ID','target_x','target_y','target_z','target_type'])

pn_ids = np.arange(0,22140)
itn_ids = np.arange(22140,27000)

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


PN2PN = conns[(conns.source_type=='PN') & (conns.target_type=='PN')]
PN2ITN = conns[(conns.source_type=='PN') & (conns.target_type=='ITN')]
ITN2PN = conns[(conns.source_type=='ITN') & (conns.target_type=='PN')]
ITN2ITN = conns[(conns.source_type=='ITN') & (conns.target_type=='ITN')]

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

