__author__ = 'Sebastian'

import metodos_t1
import pyfits
import numpy as np
from flux20_lib import *


f1 = "out/blank.fits"
f2 = "res/stellar1.dat"
hdu = pyfits.open(f1)
metodos_t1.addStellarCatalog(hdu,f2)
hdu.close()



arch   = pyfits.open(f1)
hdr    = arch[0].header
img    = arch[0].data

print(img)

from fits_lib import plot_image
plot_image(img,log_scale=True,title=r'$\mathrm{\mathbb{Objetos\,del\,cat\acute{a}logo\,marcados\,con\,signo\,\plus}}$')
