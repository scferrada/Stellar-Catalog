__author__ = 'Sebastian'


import metodos_t1
import pyfits
import numpy as np
from flux20_lib import *
from fits_lib import plot_image, get_fits_matrix, get_fits_header, print_header


f1 = "out/blank.fits"
f2 = "res/stellar.dat"
f3 = "m83.fits"


#hdu = pyfits.open(f1)
#print type(hdu[0].data)
#metodos_t1.addStellarCatalog(hdu,f2)
#hdu.close()



arch   = pyfits.open(f1,mode="update")

metodos_t1.addStellarCatalog(arch,f2)
arch.flush()
arch.close()

le = pyfits.open(f1) 
#hdr    = arch[0].header
img    = le[0].data
print img[2532][878]
print(img)

from fits_lib import plot_image
plot_image(img,log_scale=False,title=r'$\mathrm{\mathbb{Objetos\,del\,cat\acute{a}logo\,marcados\,con\,signo\,\plus}}$')
