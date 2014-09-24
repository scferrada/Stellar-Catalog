#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pyfits

def plot_image(image,interpolation="nearest",log_scale=False,title=None):

    ''' buenos colores
	'hot' 'gray' 'Greys' 'bone' 'copper' 'gist_heat' 'pink' 'summer' 'afmhot'
    '''

    if log_scale:
       min_value = np.min(image)
       if min_value <= 0: image2 = image + np.abs(min_value) + 10.0
       else: image2 = image - min_value + 10.0
       plt.imshow(np.log(image2),interpolation=interpolation)
       plt.set_cmap('hot')
       plt.colorbar()
    else:
       plt.imshow(image,interpolation=interpolation)
       plt.set_cmap('hot')
       plt.colorbar()

    if title != None:
       plt.title(str(title))

    plt.show()
    return

def get_fits_matrix(path,index=0):

    arch = pyfits.open(path)
    mtx  = arch[index].data
    return mtx

def get_fits_header(path,index=0):

    arch = pyfits.open(path)
    hdr  = arch[index].header
    resp = []
    for key in list(hdr):
        resp.append((key,hdr[key]))
    return resp

def print_header(list_header):

    for key,value in list_header:
        key_str = key + " "*(8-len(key))
        print ">> %s\t= %s" % (key_str,str(value))

