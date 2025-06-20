# XYZ File Editing
import numpy as np

def atomDict_Out(coordFile_name):
    """
    Reading XYZ file, converting into dictionary

    input:
        - file_name: .xyz file name
    output:
        - dictionary {atom species (Si, O, N, etc.) : coordinate (type=array)}
    """
    
    # Optimized Structure
    coordsList = open(coordFile_name).read().splitlines()
    allNum_atom = int(coordsList[0].split()[0]); atomDict = {}
    
    for ea_line in coordsList[2:2+allNum_atom]:
        atomType = ea_line.split()[0]
        atomCoordArray = np.asarray([float(eaCoord) for eaCoord in ea_line.split()[1:]])
    
        if atomType not in atomDict.keys():
            atomDict[atomType] = []
        atomDict[atomType].append(atomCoordArray)
        
    return atomDict
