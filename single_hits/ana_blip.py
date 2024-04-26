import tables as tab
import numpy as np
import sys
import lar_param as lar
import projection_2d as proj2d
import histograms as hist

""" get the general infos """
with tab.open_file(sys.argv[1],"r") as f:
    infos = f.get_node('/',name='infos',classname='Table')
    n_channels = infos.read(0,1,field='n_channels')[0].astype(int)
    n_view = infos.read(0,1,field='n_view')[0].astype(int)
    e_drift = infos.read(0,1,field='e_drift')[0].astype(float)
    view_nchan  = infos.read(0,1,field='view_nchan')[0].astype(int)

v_drift = lar.drift_velocity(e_drift)
print("v_drift = ", v_drift)


inname = sys.argv[1]
inname = inname[inname.rfind("/")+1:]
inname = inname[:inname.find(".h5")]
print(inname)

if(inname[:2] == "cb"):
    inname = inname[2:]

is_top = True
if(inname[:3]=="bot"):
    is_top = False


print(inname)
print('Is top? ', is_top)



sh_all, sh_tight, sh_loose = [], [], []
channel = [[] for x in range(3)]


l_trk = []
l_bary = []
n_sh_evt = []

n_evt, n_sh, n_sh_sel = 0, 0, 0
n_sh_sel_test=0
n_sh_sel_loose=0



""" loop on all h5 files """
for files in sys.argv[1:]:
    print(files)
    with tab.open_file(files, "r") as f:
        infos = f.get_node('/',name='infos',classname='Table')
        n_evt += infos.read(0,1,field='n_evt')[0].astype(int)
        event = f.root.event.read()
        n_sh_evt.extend([n for n in event['n_single_hits']])


        """ read the single hit table """
        t_sh = f.root.single_hits
        d_sh = t_sh.read()

        """ read the hit table """
        t_hits = f.root.hits
        d_hits = t_hits.read()


        n_sh += t_sh.nrows


        """ apply quality cuts on the single hits """
        """ time between hits t max between view 0 and view 1 """
        cut1 = d_sh['tdc_max'][:,1]-d_sh['tdc_max'][:,0] > 0
        cut2 = d_sh['tdc_max'][:,1]-d_sh['tdc_max'][:,0] < 35
        """ time between hits t max between view 2 and view 1 """
        cut3 = d_sh['tdc_max'][:,2]-d_sh['tdc_max'][:,1] > 0
        cut4 = d_sh['tdc_max'][:,2]-d_sh['tdc_max'][:,1] < 35
        """ time between hits t min between view 1 and view 0 """
        cut5 = d_sh['tdc_min'][:,1]-d_sh['tdc_min'][:,0] < 35
        cut6 = d_sh['tdc_min'][:,1]-d_sh['tdc_min'][:,0] > 0

        """ cut on the transverse 2D distance between single hit and closest 2D track """ 
        cut7 = d_sh['d_track_2D'] > 30.
        """ cut on the single hit barycenter-coordinate """
        """ this removes a lot of bad association """
        cut8 = d_sh['d_bary_max'] < 3.


        """ request that the single hits are not vetoed """
        """ i.e. that the single hits are isolated in each view """
        cut9  = d_sh['veto'][:,0] == False
        cut10 = d_sh['veto'][:,1] == False
        cut11 = d_sh['veto'][:,2] == False

        """ tight selection """
        cut =  cut1 & cut2 & cut3 & cut4 & cut5 & cut6 & cut7 & cut8 & cut9 & cut10 & cut11
        cut = np.asarray(cut)

        """ loose selection (no cut on veto) """
        cut_loose =  cut1 & cut2 & cut3 & cut4 & cut5 & cut6 & cut7 & cut8
        cut_loose = np.asarray(cut_loose)
                
        n_sh_sel += np.sum(cut)
        n_sh_sel_loose += np.sum(cut_loose)

        
        l_trk.extend([l for l in d_sh['d_track_2D']])
        l_bary.extend([l for l in d_sh['d_bary_max']])

        sh_all.extend([(x, y, z, p, n, q) for x, y, z, p, n, q in zip(d_sh['x'], d_sh['y'], d_sh['z'], d_sh['charge_pos'], d_sh['charge_neg'], d_sh['charge_extend'])])

        
        sh_tight.extend([(x, y, z, p, n, q) for x, y, z, p, n, q in zip(d_sh[cut]['x'], d_sh[cut]['y'], d_sh[cut]['z'], d_sh[cut]['charge_pos'], d_sh[cut]['charge_neg'], d_sh[cut]['charge_extend'])])


        sh_loose.extend([(x, y, z, p, n, q) for x, y, z, p, n, q in zip(d_sh[cut_loose]['x'], d_sh[cut_loose]['y'], d_sh[cut_loose]['z'], d_sh[cut_loose]['charge_pos'], d_sh[cut_loose]['charge_neg'], d_sh[cut_loose]['charge_extend'])])

        """ the single hits are made of assembly of hits in each views, and with th ID list one can recover the hit information, like the channel number """
        for iv in range(3):
            channel[iv].extend([d_hits[idx]['channel'] for hits in d_sh[cut_loose]['hit_IDs'] for idx in hits[iv] if idx > 0])

        
#print('nevent: ', n_evt) #I principle this should work, but I just discovered a minor bug in the reconstruction which makes this nb of event count wrong
n_evt = len(n_sh_evt)
print('nevent: ', n_evt)
print('n SH:', n_sh, '---> %.3f'%( n_sh/n_evt), ' per event')
print('Tight sel ', n_sh_sel, '---> %.3f'%( n_sh_sel/n_evt), ' per event')
print('Loose sel : ', n_sh_sel_loose, '---> %.3f'%( n_sh_sel_loose/n_evt), 'per event')

""" if you want to store some histograms uncomment the output and fstore, hstore in hist.hist calls """
#output = "results/"+inname+"_PNS_sel.h5"


hist.hist(l_trk, nbins=500, hrange=[0, 50], xlabel='SH 2D distance to 2D track [cm]', out=inname+'_blip_2Ddist_trk', show=True)
hist.hist(l_bary, nbins=400, hrange=[0, 20], xlabel='SH barycenter-coord [cm]', out=inname+'_blip_bary', show=True)


hist.hist(n_sh_evt, nbins=50, hrange=[-0.5, 50.5], xlabel='N SH per event', out=inname+'_blip_per_evt', show=True)


for iv in range(3):
    hist.hist(channel[iv], nbins=view_nchan[iv], hrange=[-0.5, view_nchan[iv]-0.5], xlabel='N SH On View '+str(iv)+' channel', out=inname+'_blip_channel_v'+str(iv), show=True)


xy_sh = [(x[0], x[1]) for x in sh_tight]
xy_sh_all = [(x[0], x[1]) for x in sh_all]
xy_sh_loose = [(x[0], x[1]) for x in sh_loose]
proj2d.proj_above_all(xy_sh_all, out=inname+"_pns_xy_all", the_title='No Selections', show=True)
proj2d.proj_above_all(xy_sh, out=inname+"_pns_xy_nom", the_title='Tight Selection', show=True)
proj2d.proj_above_all(xy_sh_loose, out=inname+"_pns_xy_loose", the_title='Loose Selection', show=True)

q_sh_all = [h[3][2] for h in sh_all]
q_sh = [h[3][2] for h in sh_tight]
q_sh_loose = [h[3][2] for h in sh_loose]


hist.hist_multi([q_sh_all, q_sh_loose, q_sh], nbins=500,  hrange=[0, 50],  xlabel=r'SH Collected Charge [fC]', out=inname+'_pns_qcoll_compare_sel', log=True, show=True, legend=['All', 'Loose', 'Tight cut'], color=['k', 'tab:blue', 'r'], stacked=False)

hist.hist(q_sh_loose, nbins=500, hrange=[0, 50], xlabel='SH Charge [fC]', out=inname+'_pns_qcoll_loose_sel', show=True)#, fstore=output, hstore='qcoll')


x = [h[0] for h in sh_tight]
hist.hist(x, 168, [-168, 168], 'SH along x', out=inname+'_PNS_x', log=False, show=True)#, fstore=output, hstore='x_proj')
y = [h[1] for h in sh_tight]
hist.hist(y, 150, [-150, 150], 'SH along y', out=inname+'_PNS_y', log=False, show=True)#, fstore=output, hstore='y_proj')
z = [h[2] for h in sh_tight]
#print(min(z), max(z))
hist.hist(z, 130, [-210, 50], 'SH along z', out=inname+'_PNS_z', log=False, show=True)#, fstore=output, hstore='z_proj')





