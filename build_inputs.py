t_sim = 10000
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
#
psg = PoissonSpikeGenerator(population='mthalamus')
psg.add(node_ids=range(22140),  # Have nodes to match mthalamus
        firing_rate=0.002,    # 15 Hz, we can also pass in a nonhomoegenous function/array
        times=(0.0, t_sim))    # Firing starts at 0 s up to 3 s
psg.to_sonata('mthalamus_spikes.h5')

psg = PoissonSpikeGenerator(population='exc_bg_bask')
psg.add(node_ids=range(4860),  # Have nodes to match mthalamus
        firing_rate=0.002,    # 15 Hz, we can also pass in a nonhomoegenous function/array
        times=(0.0, t_sim))    # Firing starts at 0 s up to 3 s
psg.to_sonata('exc_bg_bask_spikes.h5')
