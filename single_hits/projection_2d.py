import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.gridspec as gridspec
import fast_histogram as fh
import colorcet as cc
col_density = cc.cm.fire_r
from matplotlib.colors import LogNorm

def draw_proj(xy, plot_xrange, plot_yrange, plot_bins, ax, ax_col, fig):
    h_fast = fh.histogram2d(*zip(*xy),
                            range=[plot_xrange, plot_yrange],
                            bins = plot_bins)

    xy_range = plot_xrange
    xy_range.extend(plot_yrange)
    im = ax.imshow(h_fast.transpose(), origin='lower',aspect='auto', interpolation='none', extent=xy_range, cmap=col_density)
    
    cb = fig.colorbar(im, cax=ax_col, orientation='horizontal')
    cb.ax.xaxis.set_ticks_position('top')
    cb.ax.xaxis.set_label_position('top')

def scatter_start_stop(x,y, point, out):
    fig = plt.figure(figsize=(4,7))
    #gs = gridspec.GridSpec(nrows=2, ncols=3, height_ratios=[1,30])
    ax = fig.add_subplot(111)
    ax.scatter(x, y, marker='o', facecolors='none', edgecolors='k', s=8)

    xmin, xmax = -168.2625, 168.2625
    ymin, ymax = -149.1545, 149.1545
    
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('X track '+point+' [cm]')
    ax.set_ylabel('Y track '+point+' [cm]')

    plt.tight_layout()
    fig.savefig('results/run_'+out+'_tracks3D_XY_'+point+'_scatt.png', dpi=200)
    plt.show()
    plt.close()


def arrow_above(xy, ang, point, out):
    fig = plt.figure(figsize=(4,7))
    #gs = gridspec.GridSpec(nrows=2, ncols=3, height_ratios=[1,30])
    ax = fig.add_subplot(111)
    X, Y = zip(*xy)
    U = [np.cos(np.radians(k)) for k in ang]
    V = [np.sin(np.radians(k)) for k in ang]
    ax.quiver(X, Y, U, V)

    xmin, xmax = -168., 168.
    ymin, ymax = -148.896, 148.896
    
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('X track '+point+' [cm]')
    ax.set_ylabel('Y track '+point+' [cm]')

    plt.tight_layout()
    fig.savefig('results/run_'+out+'_tracks3D_XY_'+point+'_quiver.png', dpi=200)
    plt.show()
    plt.close()


def proj_above_all(xy, out, the_title='All Views Together', show=True, point=None):
    fig = plt.figure(figsize=(6,5.5))
    gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[1,30])
    
    ax = fig.add_subplot(gs[1,0])
    ax_col = fig.add_subplot(gs[0,0])


    nx = 380
    ny = 584

    xmin, xmax = -168., 168.
    ymin, ymax = -148.896, 148.896


    draw_proj(xy, [xmin, xmax], [ymin, ymax], [nx, ny], ax, ax_col, fig)

    ax.set_xlabel('x [cm]')
    ax.set_ylabel('y [cm]')
    ax.set_title(the_title)
    ax_col.set_title('Hit Density')

    if(point):
        ax.scatter(*zip(*point), marker='o', facecolors='none', edgecolors='k', s=8)        

    plt.tight_layout()
    fig.savefig('results/run_'+out+'_tracks3D_hitsXY_all_views.png', dpi=200)
    if(show):
        plt.show()
    #print(fig.get_size_inches())
    plt.close()


    
def proj_above(xy,  out, show=True):
    fig = plt.figure(figsize=(12,4.5))
    gs = gridspec.GridSpec(nrows=2, ncols=3, height_ratios=[1,30])
    
    axs = [fig.add_subplot(gs[1,i]) for i in range(3)]
    axs_col = [fig.add_subplot(gs[0,i]) for i in range(3)]


    nx = 380
    ny = 584

    xmin, xmax = -168., 168.
    ymin, ymax = -148.896, 148.896


    for i in range(3):
        
        draw_proj(xy[i], [xmin, xmax], [ymin, ymax], [nx, ny], axs[i], axs_col[i], fig)
        #axs[i].set_aspect((ymax-ymin)/(xmax-xmin))
        #print("ratio : ", (ymax-ymin)/(xmax-xmin))

        axs[i].set_xlabel('x [cm]')
        axs[i].set_ylabel('y [cm]')
        axs[i].set_title('View '+str(i))
        axs_col[i].set_title('Hit Density')

    plt.tight_layout()
    fig.savefig('results/run_'+out+'_tracks3D_hitsXY.png', dpi=200)
    if(show):
        plt.show()

    plt.close()
   


def proj_side(xz, yz, bin_dist, out, show=True, extended=False):

    fig = plt.figure(figsize=(10,4))
    gs = gridspec.GridSpec(nrows=2, ncols=2, height_ratios=[1,30])
    
    axs = [fig.add_subplot(gs[1,i]) for i in range(2)]
    axs_col = [fig.add_subplot(gs[0,i]) for i in range(2)]


    nx = 380
    ny = 584

    xmin, xmax = -168., 168.
    ymin, ymax = -148.896, 148.896

    zmin, zmax = -12.5, 12.5
    if(extended==True):
        zmin, zmax = -12.5, 42.5

    nz = int((zmax-zmin)/bin_dist)

        
    #XZ 
    i = 0
    draw_proj(xz, [xmin, xmax], [zmin, zmax], [nx, nz], axs[i], axs_col[i], fig)
    axs[i].set_xlabel('x [cm]')
    axs[i].set_ylabel('z [cm]')
    #axs[i].set_title('View '+str(i))
    axs_col[i].set_title('XZ - Hit Density')

    #YZ 
    i = 1
    draw_proj(yz, [ymin, ymax], [zmin, zmax], [ny, nz], axs[i], axs_col[i], fig)
    axs[i].set_xlabel('y [cm]')
    axs[i].set_ylabel('z [cm]')
    #axs[i].set_title('View '+str(i))
    axs_col[i].set_title('YZ - Hit Density')

    for a in axs: 
        a.axhline(11.5, lw=1, ls=':',c='k')
        a.axhline(-11.5, lw=1, ls=':',c='k')


    plt.tight_layout()
    fig.savefig('results/run_'+out+'_tracks3D_hits_XZ_YZ.png', dpi=200)
    if(show):
        plt.show()
    plt.close()
   




def proj_above_all_prof(xy, data, out, the_title='All Views Together', vmin=-1, vmax=-1, show=True):
    fig = plt.figure(figsize=(6,5.5))
    gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[1,30])
    
    ax = fig.add_subplot(gs[1,0])
    ax_col = fig.add_subplot(gs[0,0])


    nx = 190#380
    ny = 292#584

    xmin, xmax = -168., 168.
    ymin, ymax = -148.896, 148.896

    h = fh.histogram2d(*zip(*xy), weights=data,
                           range=[[xmin, xmax], [ymin, ymax]],
                           bins = [nx, ny])

    h_count = fh.histogram2d(*zip(*xy),
                           range=[[xmin, xmax], [ymin, ymax]],
                           bins = [nx, ny])

    with np.errstate(invalid='ignore'):
        h /= h_count


    #draw_proj(h.transpose(), [xmin, xmax], [ymin, ymax], [nx, ny], ax, ax_col, fig)
    if(vmin >= 0 and vmax > 0):
        im = ax.imshow(h.transpose(), origin='lower',aspect='auto', interpolation='none', extent=[xmin, xmax, ymin, ymax], cmap=col_density, vmin=vmin, vmax=vmax)#, norm=LogNorm(vmin=vmin, vmax=vmax))
    else:
        im = ax.imshow(h.transpose(), origin='lower',aspect='auto', interpolation='none', extent=[xmin, xmax, ymin, ymax], cmap=col_density)

    ax.set_xlabel('x [cm]')
    ax.set_ylabel('y [cm]')
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])


    ax_col.set_title(the_title)

    cb = fig.colorbar(im, cax=ax_col, orientation='horizontal')
    cb.ax.xaxis.set_ticks_position('top')
    cb.ax.xaxis.set_label_position('top')


    plt.tight_layout()
    fig.savefig('results/run_'+out+'.png', dpi=200)
    if(show):
        plt.show()
    plt.close()
