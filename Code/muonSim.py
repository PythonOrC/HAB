import random
import math
import pionSpectrum as ps
from concurrent.futures import ThreadPoolExecutor
import csv

nCrossing = []
e = math.e
# λ = 1200 kg/m2
lam_factor = 1200
lam = 1200 * 800/lam_factor
# ρ0 = 1.23 kg/m3
rho0 = 1.23
# H = 7570 m
H = 7570
# (dE/dx)0 = 2e-4 GeV * m^2 / kg
dEdx0 = 2e-4
# altitude 100 m intervals
deltah = 100
# m = 0.107 GeV
m = 0.107
# c = 3e8 m/s
c = 299792458
# τ = 2.2e-6 s
tau = 2.2e-6
pion_factor = 0.25

# number of pions produced by each proton
pionMult = 30

event_reduce = 8

# calculate density of air at height h
def rhoair(h):
    return rho0 * e ** (-h / H)


def lamdecay(p):
    return p / m * c * tau


def genMuon():
    r = random.random()
    t = -1 * lam * math.log(r, e)  # penetration depth
    height = -1 * H * math.log(t / (rho0 * H), e)

    if height < 0:
        return

    for i in range(28200, int(height), -deltah):
        nCrossing[i // deltah] += 1

    for i in range(pionMult):
        h = height
        ppi = ps.genPionSpectrum() * pion_factor
        pmu = 0.787 * ppi
        decay = False
        while (not decay) and (h >= 0):
            deltaE = dEdx0 * rhoair(h) * deltah
            pmu -= deltaE
            Pdecay = 1 - e ** (-1 * deltah / lamdecay(pmu))
            r = random.random()
            if pmu > 0 and r > Pdecay:
                if h <= 28200:
                    i = int(h // deltah)
                    nCrossing[i] += 1
            else:
                decay = True
            h -= deltah


for i in range(0, 28201, deltah):
    nCrossing.append(0)

with ThreadPoolExecutor() as executor:
    for i in range(1, 1000001 // event_reduce):
        executor.submit(genMuon)
        if i % (10000//event_reduce) == 0:
            print(i // (10000 // event_reduce), "%")

with open("Simulation Result.csv", "w", newline="") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["altitude", "count"])
    for i in range(0, 28200, deltah):
        if nCrossing[i // deltah] != 0:
            writer.writerow([i, nCrossing[i // deltah]])
