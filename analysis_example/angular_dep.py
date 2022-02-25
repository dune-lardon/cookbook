import matplotlib.pyplot as plt
import fast_histogram as fh
import colorcet as cc
import matplotlib.gridspec as gridspec

col_density = cc.cm.fire_r


def ang_val(data, ang_name, ang_save, ang_range, ang_bins, val_name, val_save, val_range, val_bins, out, show):
    fig = plt.figure()
    gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[1,15])
    ax = fig.add_subplot(gs[1,:])
    ax_col = fig.add_subplot(gs[0,:])


    h_fast = fh.histogram2d(*zip(*data),
                            range=[ang_range, val_range],
                            bins = [ang_bins, val_bins])

    xy_range = ang_range
    xy_range.extend(val_range)

    im = ax.imshow(h_fast.transpose(), origin='lower',aspect='auto', interpolation='none', extent=xy_range, cmap=col_density)

    cb = fig.colorbar(im, cax=ax_col, orientation='horizontal')
    cb.ax.xaxis.set_ticks_position('top')
    cb.ax.xaxis.set_label_position('top')

    ax.set_ylabel(val_name)
    ax.set_xlabel(ang_name)
    
    fig.savefig('results/'+out+'_'+ang_save+'_'+val_save+'.png',dpi=200)

    if(show==True):
        plt.show()
    plt.close()

def theta_val(data, val_name, val_save, val_range, val_bins, out,show=True):
    theta_range = [90, 180]
    theta_bins = 90
    ang_val(data, 'Theta [degree]', 'theta', theta_range, theta_bins, val_name, val_save, val_range, val_bins, out,show)


def phi_val(data, val_name, val_save, val_range, val_bins, out,show=True):
    phi_range = [-180, 180]
    phi_bins = 180
    ang_val(data, 'Phi [degree]', 'phi', phi_range, phi_bins, val_name, val_save, val_range, val_bins, out,show)
    


