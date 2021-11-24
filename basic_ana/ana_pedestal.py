import sys
import tables as tab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import statistics as stat
import math
import colorcet as cc
from matplotlib.colors import hex2color, rgb2hex


cmap = cc.cm.CET_CBL2_r

class chmap:
    def __init__(self, daq, view, chan):
        self.daq  = daq
        self.view = view
        self.chan = chan

inname = sys.argv[1]
inname = inname[inname.rfind("/")+1:]
inname = inname[:inname.find(".h5")]
print(inname)




with tab.open_file(sys.argv[1],"r") as f:
    infos = f.get_node('/',name='infos',classname='Table')
    n_channels = infos.read(0,1,field='n_channels')[0].astype(int)
    n_view = infos.read(0,1,field='n_view')[0].astype(int)
    view_nchan  = infos.read(0,1,field='view_nchan')[0].astype(int)


    chm = f.get_node('/',name='chmap',classname='Table')
    views = chm.read(0,1,field='view')[0]
    chans = chm.read(0,1,field='channel')[0]

ch_list = []
for i in range(n_channels):
    ch_list.append( chmap(i, views[i], chans[i]) )


rms_raw = []
rms_filt = []

nevt = 0

for files in sys.argv[1:]:
    with tab.open_file(files, "r") as f:
        table = f.get_node("/", name='pedestals', classname="Table")
        for r in table.iterrows():            
            rms_raw.append(r['raw_rms'])
            rms_filt.append(r['filt_rms'])
            nevt += 1

print(nevt, ' events')




rms_raw = np.asarray(rms_raw)
rms_filt = np.asarray(rms_filt)

rms_raw_mean = np.mean(rms_raw,axis=0)
rms_raw_rms = np.std(rms_raw,axis=0)
rms_filt_mean = np.mean(rms_filt,axis=0)
rms_filt_rms = np.std(rms_filt,axis=0)

fig = plt.figure(1, figsize=(12,4))
ax_std  = fig.add_subplot(111)
ch = np.linspace(0, n_channels,n_channels, endpoint=False)

ax_std.errorbar(ch, rms_raw_mean, yerr=rms_raw_rms, ecolor='k', fmt='ow', mec='k', markersize=2, label='raw')
ax_std.errorbar(ch, rms_filt_mean, yerr=rms_filt_rms, ecolor='r', fmt='ow', mec='r', markersize=2, label='filtered')

ax_std.legend()
ax_std.set_ylabel('Pedestal RMS [ADC]')
ax_std.set_xlabel('DAQ Channels')

ymin, ymax = ax_std.get_ylim()

fig.savefig('results/pedrms_daqch_'+inname+'.png')


figv = plt.figure(2, figsize=(12,4))
gs = gridspec.GridSpec(nrows=1, 
                       ncols=3)

axs  = [figv.add_subplot(gs[0,x]) for x in range(n_view)]

v_rms_raw_mean = np.zeros((n_view, max(view_nchan)))
v_rms_raw_rms = np.zeros((n_view, max(view_nchan)))
v_rms_filt_mean = np.zeros((n_view, max(view_nchan)))
v_rms_filt_rms = np.zeros((n_view, max(view_nchan)))



for i in range(n_channels):
    view, chan = ch_list[i].view, ch_list[i].chan
    if(view >= n_view or view < 0):
        continue

    v_rms_raw_mean[view, chan] = rms_raw_mean[i]
    v_rms_raw_rms[view, chan] = rms_raw_rms[i]
    v_rms_filt_mean[view, chan] = rms_filt_mean[i]
    v_rms_filt_rms[view, chan] = rms_filt_rms[i]

for iv in range(n_view):

    axs[iv].errorbar(np.linspace(0, view_nchan[iv], view_nchan[iv], endpoint=False),v_rms_raw_mean[iv,:view_nchan[iv]],yerr = v_rms_raw_rms[iv,:view_nchan[iv]], ecolor='k', fmt='ow', mec='k', markersize=2, label='raw')

    axs[iv].errorbar(np.linspace(0, view_nchan[iv], view_nchan[iv], endpoint=False),v_rms_filt_mean[iv,:view_nchan[iv]],yerr = v_rms_filt_rms[iv,:view_nchan[iv]], ecolor='r', fmt='ow', mec='r', markersize=2, label='filtered')

    axs[iv].set_ylabel('Pedestal RMS [ADC]')
    axs[iv].set_xlabel('Channel Number')
    axs[iv].set_title('View '+str(iv))    
    axs[iv].set_xlim(0,view_nchan[iv])
    axs[iv].set_ylim(ymin,ymax)

axs[-1].legend()
plt.tight_layout()
figv.savefig('results/pedrms_vch_'+inname+'.png')
plt.show()
             
