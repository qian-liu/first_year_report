from pyNN.utility import get_script_args
import pylab
import pdb
import numpy

simulator_name = get_script_args(1)[0]  
exec("from pyNN.%s import *" % simulator_name)

plot=True

extra = {'label': 'VA'}


if simulator_name == "spinnaker":
    extra["machine"] = "eiger"
    extra["debug"] = True

setup(timestep=0.1,min_delay=0.1,max_delay=4.0,**extra)


lif = {
    "v_rest":-65.0,     # mV
    "v_reset":-65.0,    # mV
    "v_thresh":-50.0,   # mV
    "tau_m":40.0,       # mS
    "cm":40.0/50.0,     # nF
    "tau_refrac":1.0,   # mS
    "i_offset":0.0,     # nA
    "tau_syn_E":20.0,   # mS
    "tau_syn_I":5.0,    # mS
}

lifIN = {
    "v_rest":-65.0,     # mV
    "v_reset":-65.0,    # mV
    "v_thresh":-50.0,   # mV
    "tau_m":40.0,       # mS
    "cm":40.0/50.0,     # nF
    "tau_refrac":1.0,   # mS
    "i_offset":0.0,     # nA
    "tau_syn_E":20.0,   # mS
    "tau_syn_I":5.0,    # mS
}
# Setup populations
spikes_in=[[50],[100]]
spikes_in_num=numpy.array([[50,100],[10,20]])

inputspikespop=Population(2, SpikeSourceArray,{'spike_times':spikes_in_num})
inputcell=Population(2, IF_curr_exp, lifIN, label="INPUT_CELL")
outputcell=Population(1, IF_curr_exp, lif, label="OUTPUT_CELL")

# Setup connection list
# pre, post, W, D

#debug
connection_list = [
(0,0,0.5,1),
(1,0,-0.5,2),
#    (0 , 0, 1.0, 1),
#    (0 , 1, 1.0, 1),
#    (0 , 2, -1.0, 1),
#    (0 , 3, 1.0, 1),
#    (0 , 4, -1.0, 1),
#    (0 , 5, 1.0, 1),
#    (1 , 8, -2.0, 1),
#    (1 , 7, -1.0, 1),
#    (5, 0, 1.0, 1),
#    (5, 1, 1.0, 1),
#    (5, 2, 1.0, 1),
#    (5, 3, 1.0, 1),
#    (5, 4, 1.0, 1),
#    (5, 5, -1.0, 1),
#    (2, 6, 1.0, 1),
#    (2, 7, 1.0, 1),
#    (2, 8, 1.0, 1),
#    (3, 6, -1.0, 1),
#    (4, 7, 1.0, 1),
#    (5, 8, -1.0, 1),

    ]

#connection_list=list()
#for i in range(100):
#    connection_list.append([i,0,0,1])
#
#connection_list[5][2]=1
#connection_list[90][2]=1

# Setup projections
#project = Projection(inputcell, outputcell, FromListConnector(connection_list))
project = Projection(inputspikespop, outputcell, FromListConnector(connection_list))

# Record population
outputcell.record_v()    
outputcell.record()    
run(200.0)
spikes=outputcell.getSpikes()
# Plot Membrane Potential
if plot==True:
    fig = pylab.figure()
    ax = fig.add_subplot(1,1,1)
    #ax.scatter(spikes[:,1],spikes[:,0], c='b')
    ax.plot(outputcell.get_v()[:,1],outputcell.get_v()[:,2], c='b')
    pylab.show()


#end()
