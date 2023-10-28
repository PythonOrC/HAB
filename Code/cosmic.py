
# find altitude (h) distribution of cosmic-ray interaction points
# implementation is simple and slow

import numpy as np 
from math import exp, log, sqrt  
import random 
import matplotlib.pyplot as plt 
from pionSpectrum import genPionSpectrum 

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--lambda_int",type=float,default=800.,help="Mean penetration depth")
    parser.add_argument("-m","--momentum_factor",type=float,default=0.25,help="Momentum factor")
    parser.add_argument("-p","--pionMult",type=float,default=30,help="Pion multiplicity")
    return parser.parse_args()

def getArea(height,countRate) :
    hLast, area = height[0], 0.
    for i in range(1,len(height)) :
        hh = height[i]
        dh = hh - hLast 
        hLast = hh
        if hh > 2500 and hh < 28000 : area += dh*countRate[i]
    return area

args = getArgs() 

H = 7570.            # mean height of atmosphere in m
lambda_int = args.lambda_int   # mean penetration depth in kg/m**2
#lambda_int = 1080.
rho0 = 1.23          # density of atmosphere at sea-level in kg/m**3
mMu = 0.107          # mass of muon in GeV/c^2
dh = 100.            # step size in meter
dEdx0 = 2.0e-4       # dEdx scale
c = 3.e8             # speed of light in m/s
tauMu = 2.2e-6       # muon lifetime  
cTau = c*tauMu       # mean decay distance for muon not including relativisitic effects 
pMin = 0.3
momentum_factor = args.momentum_factor # factor by which momentum is altered with respect to the Gardiner paper
pionMult = int(args.pionMult) 
nEvents = int(1000000/pionMult)
norm = 1000./nEvents
norm *= 1.9

hh = [] 
nBins = 1000
hist = np.zeros(nBins)   # array to track altitude crossings

for i in range(nEvents) :
    # determine the height of the interaction
    r = random.random()
    t = - lambda_int*log(r)
    h0 = -H*log(t/(rho0*H))
    ih0 = int(h0/dh)
    hist[ih0:] += 1. 
    if i < 10 : print("r={0:8.4f} t={1:10.3f} h0={2:10.3f} ".format(r,t,h0))
    hh.append(h0) 
    for j in range(pionMult) : 
        # generate a pion momentum 
        pMu = 0.787*momentum_factor*genPionSpectrum(pMin) 
        if i < 10 : print("New muon pMu={0:.3f}".format(pMu))
        h = h0
        while h > 0. and pMu > 0. :
            mfp = (pMu/mMu)*cTau
            pDecay = 1. - exp(-dh/mfp)
            r = random.random() 
            if r < pDecay : 
                if i < 10 : print("muon decay in flight")
                break 
            eMu = sqrt(pMu*pMu + mMu*mMu)
            beta = pMu/eMu
            dE = dEdx0*rho0*exp(-h/H)*dh/(beta*beta)
            #if i < 10 : print("pMu={0:.3f} eMu={1:.3f} beta={2:.3f} dE={3:.3f} ".format(pMu,eMu,beta,dE))
            eMu -= dE 
            pMu = -1.
            arg = eMu*eMu - mMu*mMu
            if arg > 0. : pMu = sqrt(arg) 
            ih = int(h/100.)
            if ih < nBins : hist[ih] += 1
            if i < 10 : print("h={0:.1f} pMu={1:.3f} mfp={2:.1f} pDecay={3:.4f} r={4:.4f} ih={5:4d} eMu={6:.3f} beta={7:.3f} dE={8:.4f}".format(
                h,pMu,mfp,pDecay,r,ih,eMu,beta,dE))
            h -= dh 

# plot the balloon data 
xx, yy = [], []
for i, line in enumerate(open('EthanCountRateVsAltitude.csv','r').readlines()[1:]) :
    vals = line.split(',')
    if vals[0].strip() == 'EOF' : break
    xx.append(float(vals[0]))
    yy.append(float(vals[1]))  

# calculate the areas of the two curves

dataArea = getArea(xx,yy)
alt = np.linspace(0.,100000.,1000)
simulationArea = getArea(alt,hist)
print("dataArea={0:.1f} simulationArea={1:.1f}".format(dataArea,simulationArea))
hist *= (dataArea/simulationArea)
    
# xx and yy are the balloon altitude and count rate data 
plt.plot(xx,yy,'b.')
plt.title("Count Rate vs. Height")
plt.xlabel("h (m)")
plt.ylabel("Rate (Hz)")
plt.grid(True)
#plt.show() 

plt.plot(alt,hist,'r-')
plt.xlim(0.,30000.)
plt.xlabel("h (m)")
plt.ylabel("Rate (a.u.)")
txt = "$\Lambda={0:.0f}$  $f_p={1:.3f}$  $M_\pi={2:d}$".format(lambda_int,momentum_factor,pionMult)
plt.text(15000.,0.4*np.max(hist),txt)

plt.show() 
#plt.savefig("l{0:d}_m{1:d}_p{2:d}".format(int(lambda_int),int(1000*momentum_factor),pionMult))
    
