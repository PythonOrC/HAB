import random

def pionSpectrum(p) :
    if p < 3 :   A, gamma = 0.070, 1.93
    elif p < 4 : A, gamma = 0.080, 2.05
    elif p < 5 : A, gamma = 0.102, 2.25
    elif p < 6 : A, gamma = 0.150, 2.50
    else : A, gamma = 0.193, 2.65
    return A/p**(gamma)

def genPionSpectrum() :
    pMin = 0.3 
    maxY = pionSpectrum(pMin)
    nTrials = 0 
    while True :
        nTrials += 1 
        #p = random.uniform(0.75, 10.)
        #p = random.uniform(0.70, 10.)
        p = random.uniform(pMin, 10.)
        y = random.uniform(0.,maxY)
        if y < pionSpectrum(p) : 
            #print("nTrials={0:d}".format(nTrials))
            return p