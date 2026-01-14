import openmc


## gets the k from any other sp file as long as terminal is in the same directory as the sp
def getk(batch):
    sp = openmc.StatePoint(f'statepoint.{batch}.h5')
    k = sp.keff
    return k

