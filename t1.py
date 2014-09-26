__author__ = 'Sebastian'


import metodos_t1 as mt
import pyfits
import numpy as np
from flux20_lib import *
from fits_lib import plot_image, get_fits_matrix, get_fits_header, print_header


f1 = "out/blank.fits"
f2 = "res/stellar.dat"
f3 = "res/galaxy.dat"

arch   = pyfits.open(f1,mode="update")

#mt.addStellarCatalog(arch,f2)
mt.addGalaxyCatalog(arch,f3)
arch.flush()
arch.close()

le = pyfits.open(f1) 
from fits_lib import plot_image
blurred_img = le[0].data
#blurred_img = mt.convolvePSF(le, 10)
#blurred_img = mt.addNoise(le, 10000)
#blurred_img = mt.addBackground(le,100)

plot_image(blurred_img,log_scale=True,title=r'$\mathrm{\mathbb{Objetos\,del\,cat\acute{a}logo\,marcados\,con\,signo\,\plus}}$')
