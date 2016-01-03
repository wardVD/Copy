from StopsDilepton.analysis.preselection import preselection
from regions import regions1D, regions3D

zMassRange=15
 
setup = {
'zMassRange':zMassRange,

'preselectionCut':{'MC':   preselection('MC',   channel='all', zWindow='offZ', zMassRange=zMassRange, triggers=True), 
                   'Data': preselection('Data', channel='all', zWindow='offZ', zMassRange=zMassRange, triggers=True)},
'regions':        regions1D

}
