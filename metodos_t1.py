# -*- coding: cp1252 -*-
__author__ = 'Sebastian'

import numpy as np
from random import gauss
import math

def mToCounts(m, m0, F0):
    FF0 = (10 ** ((m0 - m)/2.5))
    counts = FF0 * (10 ** 8 * F0)
    return counts


def radec_to_pixels(hdr, ra, dec):
    diff_ra = ra - float(hdr['CRVAL1'])
    diff_dec = dec - float(hdr['CRVAL2'])

    diff_ver = (diff_dec/float(hdr['CD2_1']) - diff_ra/float(hdr['CD1_1']))/(float(hdr['CD2_2'])/float(hdr['CD2_1']) - float(hdr['CD1_2'])/float(hdr['CD1_1']))
    diff_hor = (diff_dec/float(hdr['CD2_2']) - diff_ra/float(hdr['CD1_2']))/(float(hdr['CD2_1'])/float(hdr['CD2_2']) - float(hdr['CD1_1'])/float(hdr['CD1_2']))

    calc_ver = float(hdr['CRPIX2']) + diff_ver
    calc_hor = float(hdr['CRPIX1'])+ diff_hor

    return calc_ver, calc_hor


def addStar(hdu, m, ra, dec):
    count = mToCounts(m, 20, hdu[0].header['FLUX20'])
    ver, hor = radec_to_pixels(hdu[0].header, ra, dec)
    max_ver, max_hor = hdu[0].data.shape
    if 0 <= ver < max_ver and 0 <= hor < max_hor:
        #print ("added %d to %d, %d" % (count, ver, hor))
        hdu[0].data[ver][hor] = count
        i = 1


def addStellarCatalog(hdu, catalog):
    stars = open(catalog, "r")
    for star in stars:
        data = star.split("\t")
        magnitude = data[3]
        ra = data[1]
        dec = data[2]
        addStar(hdu, float(magnitude), float(ra), float(dec))


def addBackground(hdu, bg):
    max_ver, max_hor = hdu[0].data.shape
    img = hdu[0].data
    for ver in range(max_ver):
        for hor in range(max_hor):
            img[ver][hor] += bg

def convolvePSF(hdu, sigma_psf):
    import scipy.ndimage as ndimage
    return ndimage.gaussian_filter(hdu[0].data, sigma = sigma_psf, order = 0)

def addNoise(hdu, sigma_noise):
    img = hdu[0].data
    val = gauss(0,sigma_noise)
    print val
    img += val
    img += np.random.poisson(sigma_noise)
    return img

def Gamma(x): # Gamma(x) = (x-1)!
    return math.factorial(x-1)


def addGalaxy(hdu, m, ra, dec, n, Re, el, tetha):
    
    
    counts = mToCounts(m, 20,hdu[0].header['FLUX20'])
    Ln = counts

    bn = 2*n-0.324
    Io = Ln*bn**(2*n)/( Re**2*2*math.pi*n*Gamma(2*n)*(1-el) )
    

    ver_c, hor_c = radec_to_pixels(hdu[0].header,ra, dec) 
    max_ver, max_hor = hdu[0].data.shape
    
    # ver=ra     hor=dec
    # ver=x      hor=y
    
    ver=-4*Re+ver_c
    
    while ver <= 4*Re+ver_c:
        
        hor = -4*Re+hor_c
                
        while hor <= 4*Re+hor_c:
            
            #print ver**2+hor**2<= (4*Re)**2
            # if: el pixel esta dentro de la imagen y dentro de un circulo de r=4Ro
            if 0 <= ver < max_ver and 0 <= hor < max_hor and ver**2+hor**2> (4*Re)**2:
                Xi_cuad = ( (ver-ver_c)*math.cos(tetha)+(hor-hor_c)*math.sin(tetha) )**2+ ( ( (ver-ver_c)*math.sin(tetha)-(hor-hor_c)*math.cos(tetha) )/(1-el) )**2
                #print Xi_cuad
                Xi = math.sqrt(Xi_cuad)
                #print Xi
                countPix = Io*math.exp( -bn*(Xi/Re)**(1/n) )
                #print countPix
                hdu[0].data[ver][hor] = countPix
                            
            hor = hor+1
            
        ver = ver+1


def addGalaxyCatalog(hdu, catalog):
        galaxies = open(catalog, "r")
        for galaxy in galaxies:
            data = galaxy.split("\t")
            ra        = data[1]
            dec       = data[2]
            magnitude = data[3]
            SED       = data[4]
            z         = data[5]
            typ       = data[6]
            n         = data[7]
            Re        = data[8]
            el        = data[9]
            tetha     = data[10]
            addGalaxy(hdu, float(magnitude), float(ra), float(dec), float(n), float(Re), float(el), float(tetha))
