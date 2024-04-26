import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.gridspec as gridspec
import fast_histogram as fh
import colorcet as cc
from scipy.optimize import curve_fit
import store_hist as store
import matplotlib.colors as mplc

col_density = cc.cm.fire_r
col_map = cc.cm.linear_tritanopic_krjcw_5_95_c24_r

#import gaus_fit as gf
def gaussian(x, amplitude, mean, standard_deviation):
    return amplitude * np.exp( - (x - mean)**2 / (2*standard_deviation ** 2))


def gaussian_line(x, amplitude, mean, standard_deviation, a, b):
    return a*x+b+amplitude * np.exp( - (x - mean)**2 / (2*standard_deviation ** 2))

def expo(x, A, tau):
    return A*np.exp(-x/tau)

def hist(val, nbins, hrange, xlabel, out, fstore='', hstore='', log=False, show=False, vlines=[]):
    
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(111)
    
    h, bins, _ = ax.hist(val, bins = nbins, range = hrange, histtype='stepfilled', fc='None', edgecolor='k',log=log)


    ax.set_xlabel(xlabel)
    if(len(fstore)>0 and len(hstore)>0):
        store.store(fstore, h, hstore)#'len_path')

    for v in vlines :
        ax.axvline(v, c='r', ls='dashed')
    #ax.legend()
    plt.tight_layout()
    fig.savefig('results/run_'+out+'.png', dpi=200)
    if(show):
        plt.show()
    plt.close()


def hist_multi(data, nbins, hrange, xlabel, out, fstore='', hstore='', log=False, show=False, legend=[], color=[], stacked=False):
    
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(111)

    if(stacked == True):
        h, bins, _ = ax.hist(data, bins = nbins, range = hrange, histtype='stepfilled',  color=color,log=log, label=legend, stacked=True)
    else:
        i = 0
        for val,leg,c in zip(data, legend, color):
            h, bins, _ = ax.hist(val, bins = nbins, range = hrange, histtype='stepfilled', fc='None', edgecolor=c,log=log, label=leg)

            if(len(fstore)>0 and len(hstore)>0):
                store.store(fstore, h, hstore[i])#'len_path')
            i = i+1

    ax.set_xlabel(xlabel)

    ax.legend(frameon=False, loc='upper right')
    plt.tight_layout()
    fig.savefig('results/run_'+out+'.png', dpi=200)
    if(show):
        plt.show()
    plt.close()

def hist_text(data,  xlabel, out, log=False, show=False):
    labels, counts = np.unique(data, return_counts=True)
    ticks = range(len(counts))
    print(ticks, labels)
    
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(111)
    
    ax.bar(ticks, counts, align='center', edgecolor="k", fc='None')
    ax.set_xticks(ticks, labels)
    
    ax.set_xlabel(xlabel)

    plt.tight_layout()
    fig.savefig('results/run_'+out+'.png', dpi=200)
    if(show):
        plt.show()
    plt.close()

    




def hist_per_view(val, nbins, hrange, xlabel, out, fstore='', hstore='', log=False, show=False):
    
    fig = plt.figure(figsize=(6,4))
    gs = gridspec.GridSpec(nrows=1, ncols=3)
    
    ax = [fig.add_subplot(gs[0,i]) for i in range(3)]

    for i in range(3):
    
        h, bins, _ = ax[i].hist(val[i], bins = nbins, range = hrange, histtype='stepfilled', fc='None', edgecolor='k',log=log)
        #print('--> Bins ', bins[:3], 'binning ', bins[1]-bins[0])

        ax[i].set_xlabel(xlabel)
        ax[i].set_title('View '+str(i))
        if(len(fstore)>0 and len(hstore)>0):
            store.store(fstore, h, hstore+'_v'+str(i))#'len_path')

    #ax.legend()
    plt.tight_layout()
    fig.savefig('results/run_'+out+'.png', dpi=200)
    if(show):
        plt.show()
    plt.close()
    



def hist_and_fit(val, nbins, hrange, xlabel, out, show=True):
    
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(111)
    
    h, bins, _ = ax.hist(val, bins = nbins, range = hrange, histtype='stepfilled', fc='None', edgecolor='k')
    binw = bins[1]-bins[0]
    print('hrange : ', hrange)
    print(binw, bins[0], bins[-1], " binw/2", binw/2)

    fmin, fmax = 130, 150 #crp5-feb
    #fmin, fmax = 145, 153 #crp2-june
    #fmin, fmax = 150, 155 #crp2-june

    #fmin, fmax = 148, 158
    #fmin, fmax = 150, 160
    #fmin, fmax = 10,30#145, 155
    #h, bfit = np.histogram(val, bins = nbfit, range = [145,155])
    
    #h, bfit = np.histogram(val, bins = nbfit, range = [fmin, fmax])
    #bfit_c = bfit[:-1] + np.diff(bfit) / 2

    bfit_c =  bins[:-1] + binw / 2
    print(bfit_c)
    mu = bfit_c[np.argmax(h)]
    std = np.std(val)#10
    hmax = np.max(h)
    print("rough guesses ", mu, std, ' max ', hmax)
    print("bfit lim", bfit_c[0], bfit_c[-1])
    ax.axvline(mu, ls='dashed', c='steelblue')
    plt.tight_layout()
    fig.savefig('results/run_'+out+'_nofit.png', dpi=200)

    h_err = [np.sqrt(x) if x > 0 else 1 for x in h]
    ##pres, pcov = curve_fit(gaussian_line, bfit_c, h, sigma=h_err, p0=[1., 0, 1., mu, std], bounds=([-30, 0, 0, mu-std, 0.], [30, 1000, 1.5*hmax, mu+std, 5*std]))
    #pres, pcov = curve_fit(gaussian_line, bfit_c, h, sigma=h_err, p0=[1., mu, std, 1., 0], bounds=([0, mu-std, 0., -30, 0], [1.5*hmax, mu+std, 5*std, 30, 1000]))
    pres, pcov = curve_fit(gaussian, bfit_c, h, p0=[1., mu, std], bounds=([ 0, mu-std, 0.], [ 1.5*hmax, mu+std, 5*std])) #, sigma=h_err


    perr = np.sqrt(np.diag(pcov))
    print('\n Gaussian fit : ')
    #[print(s, ' : ', v, ' +/- ', e) for s, v, e in zip(['A','mu','sig', 'a', 'b'], pres, perr)]
    [print(s, ' : ', v, ' +/- ', e) for s, v, e in zip(['A','mu','sig'], pres, perr)]


    #xfit = np.linspace(hrange[0], hrange[-1], 200)
    #xfit = np.linspace(145, 155, 200)
    xfit = np.linspace(fmin, fmax, 200)
    #ax.plot(xfit, gaussian(xfit, *pres), c='red', 
    ax.plot(bfit_c, gaussian(bfit_c, *pres), c='red', 
            label=r"$\mu$ = %.1f $\pm$ %.1f"%(pres[1], perr[1])
            +"\n" +
            r"$\sigma$ = %.1f $\pm$ %.1f"%(pres[2], perr[2]))


    ax.set_xlabel(xlabel)
    
    #ax.axvline(154.51, c='steelblue', label='t nominal')
    ax.legend()
    plt.tight_layout()
    fig.savefig('results/run_'+out+'.png', dpi=200)
    if(show):
        plt.show()
    plt.close()




def hist2d_zip(val, nbins, hrange, labels, cmap=col_density, out="", lines=[], log=False):
    return hist2d(valA=val, valB=[], nbins=nbins, hrange=hrange, labels=labels, cmap=cmap, out=out, lines=lines, log=log)

    
def hist2d(valA, valB, nbins, hrange, labels, cmap=col_density, out="", lines=[], log=False):

    fig = plt.figure(figsize=(7,5))
    gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[1,30])

    
    ax = fig.add_subplot(gs[1,0])
    ax_col = fig.add_subplot(gs[0,0])

    if(len(valB) == len(valA)):
       h_fast = fh.histogram2d(valA, valB,
                               range=hrange, bins=nbins)
    else:
       h_fast = fh.histogram2d(*zip(*valA),
                               range=hrange, bins=nbins)
    

    xy_range = hrange[0]
    xy_range.extend(hrange[1])
    if(log==False):
        im = ax.imshow(h_fast.transpose(), origin='lower',aspect='auto', interpolation='none', extent=xy_range, cmap=col_map)
    else:
        im = ax.imshow(h_fast.transpose(), origin='lower',aspect='auto', interpolation='none', extent=xy_range, cmap=col_map, norm=mplc.LogNorm())
    cb = fig.colorbar(im, cax=ax_col, orientation='horizontal')
    cb.ax.xaxis.set_ticks_position('top')
    cb.ax.xaxis.set_label_position('top')

    if(len(lines)>0):
        ax.plot(lines[0], lines[1], c='k', ls='dashed')
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])

    plt.tight_layout()
    fig.savefig('results/run_'+out+'.png', dpi=200)
    plt.show()
    plt.close()


def hist2d_ang_3v(theta, phi, val, nbin, the_range, name, out):
    ang = [[-41.67,138.33],[-90,90],[0]]

    fig = plt.figure(figsize=(12,8))
    gs = gridspec.GridSpec(nrows=3,ncols=2)
    ax_th = []
    ax_ph = []
    for iv in range(3):
        ax_th.append(fig.add_subplot(gs[iv,0]))
        ax_th[-1].hist2d(theta, val[iv], bins=[90,nbin],range=[[90,180],the_range],cmap=col_density)
        ax_th[-1].set_xlabel(r'Theta$^{*}$ [degree]')
        ax_th[-1].set_ylabel(name+' View '+str(iv))
        ax_ph.append(fig.add_subplot(gs[iv,1]))
        ax_ph[-1].hist2d(phi, val[iv], bins=[180,nbin],range=[[-180,180],the_range],cmap=col_density)
        ax_ph[-1].set_xlabel(r'Phi$^{*}$ [degree]')
        ax_ph[-1].set_ylabel(name+' View '+str(iv))
        for a in ang[iv]:
            ax_ph[-1].axvline(a,color="k",ls='dashed',lw=0.5)#,zorder=-200)

    plt.tight_layout()
    fig.savefig('results/run_'+out+'.png', dpi=200)
    plt.show()
    plt.close()
    



def hist_and_expo_fit(val, nbins, hrange, xlabel, out, fit_range, show=True):
    
    fig = plt.figure(figsize=(6,4))
    ax = fig.add_subplot(111)

    full_bin_w = (hrange[1]-hrange[0])/nbins
    #print('bin width', full_bin_w)
    fit_nbins = int((fit_range[1]-fit_range[0])/full_bin_w)
    #print('fit will use ', fit_nbins)
    """ histogram in a restricted range """
    h, bins = np.histogram(val, bins = fit_nbins, range = fit_range)
    
    #h, bins, _ = ax.hist(val, bins = nbins, range = hrange, histtype='stepfilled', fc='None', edgecolor='k')
    binw = bins[1]-bins[0]
    bfit_c =  bins[:-1] + binw / 2
    
    #print('fit range : ', fit_range)
    #print(binw, bins[0], bins[-1], " binw/2", binw/2)
    #print('bin centers : ', bfit_c)

    tau = 10
    hmax = np.max(h)

    h_err = [np.sqrt(x) if x > 0 else 1 for x in h]

    pres, pcov = curve_fit(expo, bfit_c, h, p0=[hmax, tau], bounds=([ 0, 1e-3], [ 10*hmax, 1000])) #, sigma=h_err
    perr = np.sqrt(np.diag(pcov))

    
    print('\n Expo fit : ')
    [print(s, ' : ', v, ' +/- ', e) for s, v, e in zip(['A','tau'], pres, perr)]
    A, tau = pres[0], pres[1]
    print('Integral expo')
    integral = (-tau)*(expo(hrange[1], A, tau)-expo(hrange[0], A, tau))/full_bin_w
    print('--->', integral)

    xfit = np.linspace(hrange[0], hrange[1], 200)
    ax.hist(val, bins = nbins, range = hrange, histtype='stepfilled', fc='None', edgecolor='k')
    #ax.plot(xfit, gaussian(xfit, *pres), c='red', 
    ax.plot(xfit, expo(xfit, *pres), c='red', 
            label=r"$A$ = %.1f $\pm$ %.1f"%(pres[0], perr[0])
            +"\n" +
            r"$\tau$ = %.1f $\pm$ %.1f cm"%(pres[1], perr[1]))
    

    ax.set_xlabel(xlabel)

    ax.legend()
    plt.tight_layout()
    fig.savefig('results/run_'+out+'.png', dpi=200)
    if(show):
        plt.show()
    plt.close()
