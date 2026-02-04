import openmc

def getk(Batches):
    sp = openmc.StatePoint(f'statepoint.{Batches}.h5')
    k = sp.keff
    print(f'Keff is {k}')

getk(2060) #solid 0.2 maybe 0.4
getk(2061) #annular 0.4
getk(2062) #ann 0.8
getk(2063) #ann 0.65 and added some bp to the high assembly
getk(2064) #ann 0.8 added bp toi the middle top ass