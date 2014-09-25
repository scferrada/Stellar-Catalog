__author__ = 'Sebastian'


import metodos_t1 as mt
import pyfits
import numpy as np
from flux20_lib import *
from fits_lib import plot_image, get_fits_matrix, get_fits_header, print_header


f1 = "out/blank.fits"
f2 = "res/stellar.dat"

arch   = pyfits.open(f1,mode="update")

mt.addStellarCatalog(arch,f2)
arch.flush()
arch.close()

le = pyfits.open(f1) 
from fits_lib import plot_image
blurred_img = mt.convolvePSF(le, 5)
plot_image(blurred_img,log_scale=True,title=r'$\mathrm{\mathbb{Objetos\,del\,cat\acute{a}logo\,marcados\,con\,signo\,\plus}}$')
