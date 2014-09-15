__author__ = 'Sebastián'

def mToCounts(m, m0, F0):
    FF0 = (10 ** ((m0 - m)/2.5))
    counts = FF0 * (10 ** 8)
    return counts

