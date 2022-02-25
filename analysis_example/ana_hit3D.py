import tables as tab
import numpy as np
import sys

import angular_dep as ang
import time


tstart = time.time()

inname = sys.argv[1]
inname = inname[inname.rfind("/")+1:]
inname = inname[:inname.find(".h5")]
print(inname)


with tab.open_file(sys.argv[1],"r") as f:
    infos = f.get_node('/',name='infos',classname='Table')
    n_channels = infos.read(0,1,field='n_channels')[0].astype(int)
    n_view = infos.read(0,1,field='n_view')[0].astype(int)
    e_drift = infos.read(0,1,field='e_drift')[0].astype(float)


theta, phi = [], []
#theta_e, phi_e = [], []

#view = [[] for i in range(n_view)]
hits = [[] for i in range(n_view)]


nevt, ntot, nsel = 0, 0, 0

for files in sys.argv[1:]:
    with tab.open_file(files, "r") as f:
        infos = f.get_node('/',name='infos',classname='Table')
        nevt += infos.read(0,1,field='n_evt')[0].astype(int)
        
        t_trk  = f.root.tracks3d
        path = []
        for i in range(n_view):
            path.append(f.get_node('/trk3d_v'+str(i)))

        t_hits = f.root.hits
        d_hits = t_hits.read()

        data = t_trk.read()

        """ 
        select only late tracks that enters from the anode
        """
        cut1 = data['z0_corr'] < 9999.
        cut2 = data['z0_corr'] > 0
        """ remove too horizontal tracks """
        cut3 =  data['theta_ini'] > 100

        """ long enough tracks and well defined in at least one view """
        cut4 = np.max(data['len_straight']) > 20.
        cut5 = np.max(data['n_hits']) > 10

        cut6 = data['n_matched']>1

        """ remove badly matched tracks """
        cut7 = data['d_match'] < 2.5

        cut = cut1 & cut2 & cut3 & cut4 & cut5 & cut6 & cut7

        ntot += t_trk.nrows
        cut = np.asarray(cut)
        nsel += np.sum(cut)

        theta.extend([t for t in data[cut]['theta_ini']])
        phi.extend([p for p in data[cut]['phi_ini']])

        for i in range(n_view):
            h = path[i][cut]
            #view[i].extend([ (x[0], x[1], x[2]+z, np.fabs(x[3])/x[4]) for xr,z in zip(h,data[cut]['z0_corr']) for x in xr[1:-2]])

            for xr in h:
                """ First and last hits are removed because they may be partly defined"""
                hits[i].append([(d_hits[int(x[5])]['fC_max'], d_hits[int(x[5])]['fC_min'], d_hits[int(x[5])]['charge_pos'], d_hits[int(x[5])]['charge_neg'], d_hits[int(x[5])]['tdc_min']-d_hits[int(x[5])]['tdc_max']) for x in xr[1:-2]])

"""
hits is an array(for the 3 views) of array (for each seleced 3D tracks)

len(hits[view]) == len(theta)
the hits array is a tuple (fC_max, fC_min, charge_pos, charge_neg, dt (min-max) )
"""

print('Nevents: ', nevt, ' Ntracks: ', ntot, ' Nsel: ', nsel)
print('took ', time.time()-tstart, 's to analyse ', len(sys.argv[1:]), 'files')

""" 
to plot variables, one have to 'flatten' the array to give a theta/phi correspondance to each hit point
"""

for iv in range(2):
    theta_max = [(t,x[0]) for t,h in zip(theta, hits[iv]) for x in h]
    ang.theta_val(theta_max, 'Max Hit Charge [fC]', 'fC_max_v'+str(iv), [0,1], 100, inname, False)

    theta_min = [(t,x[1]) for t,h in zip(theta, hits[iv]) for x in h]
    ang.theta_val(theta_min, 'Min Hit Charge [fC]', 'fC_min_v'+str(iv), [-1,0], 100, inname,False)

    theta_pos = [(t,x[2]) for t,h in zip(theta, hits[iv]) for x in h]
    ang.theta_val(theta_pos, 'Pos Hit Charge [fC]', 'pos_charge_v'+str(iv), [0,5], 250, inname, False)

    theta_neg = [(t,x[3]) for t,h in zip(theta, hits[iv]) for x in h]
    ang.theta_val(theta_neg, 'Neg Hit Charge [fC]', 'neg_charge_v'+str(iv), [-5,0], 250, inname,False)


    theta_ratio = [(t,(x[0]-x[1])/(x[2]+np.fabs(x[3]))) for t,h in zip(theta, hits[iv]) for x in h]
    ang.theta_val(theta_ratio, r'Ratio [$\Delta$Peak/$\Sigma$|Charge|]', 'ratio_v'+str(iv), [0,0.2], 100, inname,False)


    theta_dt = [(t,x[4]) for t,h in zip(theta, hits[iv]) for x in h]
    ang.theta_val(theta_dt, r'Peak $\Delta$t [ticks]', 'dt_v'+str(iv), [0,50], 51, inname,True)


    phi_max = [(t,x[0]) for t,h in zip(phi, hits[iv]) for x in h]
    ang.phi_val(phi_max, 'Max Hit Charge [fC]', 'fC_max_v'+str(iv), [0,1], 100, inname, False)

    phi_min = [(t,x[1]) for t,h in zip(phi, hits[iv]) for x in h]
    ang.phi_val(phi_min, 'Min Hit Charge [fC]', 'fC_min_v'+str(iv), [-1,0], 100, inname,False)


    phi_pos = [(t,x[2]) for t,h in zip(phi, hits[iv]) for x in h]
    ang.phi_val(phi_pos, 'Pos Hit Charge [fC]', 'pos_charge_v'+str(iv), [0,5], 250, inname, False)

    phi_neg = [(t,x[3]) for t,h in zip(phi, hits[iv]) for x in h]
    ang.phi_val(phi_neg, 'Neg Hit Charge [fC]', 'neg_charge_v'+str(iv), [-5,0], 250, inname,False)


    phi_ratio = [(t,(x[0]-x[1])/(x[2]+np.fabs(x[3]))) for t,h in zip(phi, hits[iv]) for x in h]
    ang.phi_val(phi_ratio, r'Ratio [$\Delta$Peak/$\Sigma$|Charge|]', 'ratio_v'+str(iv), [0,0.2], 100, inname,False)


    phi_dt = [(t,x[4]) for t,h in zip(phi, hits[iv]) for x in h]
    ang.phi_val(phi_dt, r'Peak $\Delta$t [ticks]', 'dt_v'+str(iv), [0,50], 50, inname,False)
