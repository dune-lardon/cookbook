import numpy as np
import fast_histogram as fh
import colorcet as cc
import tables as tab

def store(filename, val, name):
    fout = tab.open_file(filename, 'a')    
    fout.create_carray('/', name, obj=val)
    fout.close()
