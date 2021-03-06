#!/usr/bin/env python
# encoding: utf-8
import numpy as np
def magnitud_con_flux20(cuentas,f20):
	# usamos como vimos en clases: F/F0 = counts/(10**8 * flux20)
	FF0 = cuentas / ( 10**8 * f20 )
	# calculamos la magnitud
	mag = -2.5 * np.log10(FF0)
	return mag
