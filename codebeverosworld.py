## Welkom in Bévèro's World
from BeverosWorld import start, snelheid, stap, draai_links, draai_rechts, einde_bereikt, muur_voor_mij, \
    muur_rechts_van_mij, muur_links_van_mij
# from BeverosWorld import start_eigen_maze
from BeverosWorld import plaats_hier, ding_hier, Arrow, ik, verwijder_ding
from BeverosWorld import begin_spoorzoeker, kijk_naar, route_zien
import time


##########################################
# 🚨 BOVENSTAANDE CODE NIET BEWERKEN 🚨 #
##########################################


########
## Functies
####

# draai 180 graden om
def draai_om():
    draai_links()
    draai_links()


# houd rechts aan = ontsnappen
def ontsnap_uit_doolhof():
    if not muur_rechts_van_mij():  # rechtsaf
        draai_rechts()
        plaats_hier(Arrow, ik().facing)
        stap()
    elif not muur_voor_mij():  # rechtdoor
        plaats_hier(Arrow, ik().facing)
        stap()
    elif not muur_links_van_mij():  # linksaf
        draai_links()
        plaats_hier(Arrow, ik().facing)
        stap()
    else:  # doodlopend = omkeren
        draai_om()


# zet stappen tot er een muur voor je staat
def loop_tot_einde():
    while not muur_voor_mij():
        stap()


########
## Hoofdprogramma
####

# Nieuw level
start(101)
snelheid(0)

# Loop eerst tot er rechts van je een muur staat,
# want anders werkt het "ontsnap_uit_doolhof" algoritme niet.
loop_tot_einde()
while not muur_rechts_van_mij():
    draai_rechts()

# Ontsnap uit doolhof:
while not einde_bereikt():
    pijl = ding_hier(Arrow)
    if pijl == None:
        ontsnap_uit_doolhof()
    else:
        if abs(ik().facing - pijl.facing) == 180:
            verwijder_ding(pijl)
        else:
            draai_om()
            stap()


#begin miereneter
begin_spoorzoeker()
snelheid(20)

route = [ ik().pos ]
while not einde_bereikt():
    pijl = ding_hier(Arrow)
    kijk_naar(ik(), pijl.facing)
    stap()
    route.append( ik().pos )
route_zien(route)
time.sleep(5)
