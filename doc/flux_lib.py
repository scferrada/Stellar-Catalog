#!/usr/bin/env python
# encoding: utf-8
import numpy as np
def magnitud_con_extincion(cuentas,exptime,aa,kk,airmass):
	# como vimos en clases: F/F0 = counts/exptime * 10 ** ( 0.4 * ( aa + kk * airmass ) )
	FF0 = cuentas/exptime * 10 ** ( 0.4*(aa + kk * airmass) )
	# Cálculo de magnitud
	mag = -2.5 * np.log10(FF0)
	return mag
